from adrf.serializers import ModelSerializer
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import FileExtensionValidator
from apps.v1.shared.enums import AuthStatus, AuthType
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound

from apps.v1.shared.utility import check_username_phone_email, send_email, send_phone_code, check_user_type
from .models import Profile, User, UserConfirmation
from apps.v1.users.tasks import process_user_photo

class SignUpSerializer(ModelSerializer):
    username_phone_email = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = list(
            f.name for f in User._meta.fields if f.name not in ('password', 'is_staff', 'is_superuser'))
        fields += ('username_phone_email',)
        extra_kwargs = {
            'auth_type': {'read_only': True, 'required': False},
            'auth_status': {'read_only': True, 'required': False},
        }

    def create(self, validated_data):
        verify_value = validated_data.pop("verify_value", None)
        auth_type = validated_data.pop("auth_type", None)
        password = validated_data.pop("password", None)

        # Email/phone ajratilgan bo‘lsa, tozalaymiz
        validated_data.pop("username_phone_email", None)

        # user create
        user = User(auth_type=auth_type, **validated_data)
        if password:
            user.set_password(password)
        user.save()

        # verify code yaratish va yuborish
        code = user.create_verify_code(auth_type, verify_value=verify_value)
        if auth_type == AuthType.VIA_EMAIL:
            send_email(verify_value, code)
        elif auth_type == AuthType.VIA_PHONE:
            if False in send_phone_code(verify_value, code).values():
                raise ValidationError({
                    "message": "Xatolik yuz berdi. Iltimos qaytadan urinib ko‘ring, yoki admin bilan bog‘laning"
                })

        return user

    def validate(self, data):
        super(SignUpSerializer, self).validate(data)
        data = self.auth_validate(data)
        return data

    @staticmethod
    def auth_validate(data):
        user_input = str(data.get('username_phone_email')).lower()
        input_type = check_username_phone_email(user_input)
        if input_type not in ["email", "phone"]:
            raise ValidationError({
                'message': "You must send a valid email or phone number"
            })

        data['auth_type'] = AuthType.VIA_EMAIL if input_type == "email" else AuthType.VIA_PHONE
        data['verify_value'] = user_input  # Save it for sending code, not for saving on the model
        return data

    def validate_username_phone_email(self, value):
        # return value.lower()
        value = value.lower()
        # ic(value)
        if value and User.objects.filter(email=value, auth_status__in=[AuthStatus.CODE_VERIFIED, AuthStatus.DONE, AuthStatus.DONE]).exists():
            data = {
                "message": "Bu email allaqachon ma'lumotlar bazasida bor"
            }
            raise ValidationError(data)
        elif value and User.objects.filter(phone=value, auth_status__in=[AuthStatus.CODE_VERIFIED, AuthStatus.DONE, AuthStatus.DONE]).exists():
            data = {
                "message": "Bu telefon raqami allaqachon ma'lumotlar bazasida bor"
            }
            raise ValidationError(data)

        return value

    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data["next_step"] = "Verify code sent to your email or phone"
        data.update(instance.token())

        return data

class ChangeUserInformation(serializers.Serializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)
        if password !=confirm_password:
            raise ValidationError(
                {
                    "message": "Parolingiz va tasdiqlash parolingiz bir-biriga teng emas"
                }
            )
        if password:
            validate_password(password)
            validate_password(confirm_password)

        return data

    def validate_username(self, username):
        if len(username) < 5 or len(username) > 30:
            raise ValidationError(
                {
                    "message": "Username must be between 5 and 30 characters long"
                }
            )
        if username.isdigit():
            raise ValidationError(
                {
                    "message": "This username is entirely numeric"
                }
            )
        return username

    def update(self, instance, validated_data):

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.password = validated_data.get('password', instance.password)
        instance.username = validated_data.get('username', instance.username)
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        if instance.auth_status == AuthStatus.CODE_VERIFIED:
            instance.auth_status = AuthStatus.DONE
        instance.save()
        return instance

class ChangeUserPhotoSerializer(serializers.Serializer):
    photo = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=[
        'jpg', 'jpeg', 'png', 'heic', 'heif'
    ])])

    def update(self, instance, validated_data):
        photo = validated_data.get('photo')
        if photo:
            instance.photo = photo
            instance.auth_status = AuthStatus.DONE
            instance.save()

            # ✅ Celery taskni chaqiramiz
            process_user_photo.delay(instance.id)

        return instance

class LoginSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['userinput'] = serializers.CharField(required=True)
        self.fields['username'] = serializers.CharField(required=False, read_only=True)

    def auth_validate(self, data):
        user_input = data.get('userinput')  # email, phone, username
        if check_user_type(user_input) == 'username':
            username = user_input
        elif check_user_type(user_input) == "email":  # Anora@gmail.com   -> anOra@gmail.com
            user = self.get_user(email__iexact=user_input) # user get method orqali user o'zgartiruvchiga biriktirildi
            username = users.username
        elif check_user_type(user_input) == 'phone':
            user = self.get_user(phone=user_input)
            username = users.username
        else:
            data = {
                'success': True,
                'message': "Siz email, username yoki telefon raqami jonatishingiz kerak"
            }
            raise ValidationError(data)

        authentication_kwargs = {
            self.username_field: username,
            'password': data['password']
        }
        # user statusi tekshirilishi kerak
        current_user = User.objects.filter(username__iexact=username).first()  # None

        if current_user is not None and current_user.auth_status in [AuthStatus.NEW, AuthStatus.CODE_VERIFIED]:
            raise ValidationError(
                {
                    'message': "Siz royhatdan toliq otmagansiz!"
                }
            )
        user = authenticate(**authentication_kwargs)
        if user is not None:
            self.user = user
        else:
            raise ValidationError(
                {
                    'message': "Sorry, login or password you entered is incorrect. Please check and trg again!"
                }
            )

    def validate(self, data):
        self.auth_validate(data)
        if self.user.auth_status not in [AuthStatus.DONE, AuthStatus.DONE]:
            raise PermissionDenied("Siz login qila olmaysiz. Ruxsatingiz yoq")
        data = self.user.token()
        data['auth_status'] = self.user.auth_status
        data['full_name'] = self.user.full_name
        return data

    def get_user(self, **kwargs):
        users = User.objects.filter(**kwargs)
        # ic(user)

        if not users.exists():
            raise ValidationError(
                {
                    'message': "User account not found"
                }
            )

        if users.count() > 1:
            users = users.filter(auth_status=AuthStatus.DONE)

            if users.count() > 1:
                raise ValidationError(
                    {
                        'message': "Duplicate user accounts found"
                    }
                )

        return users.first()

class LoginRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        try:
            refresh = RefreshToken(attrs['refresh'])
        except TokenError:
            raise ValidationError({'refresh': 'Token noto‘g‘ri yoki muddati tugagan'})

        data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
        return data

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class ResetPasswordSerializer(serializers.Serializer):
    username_phone_email = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        username_phone_email = attrs.get('username_phone_email', None)
        if username_phone_email is None:
            raise ValidationError(
                {
                    'message': "Email yoki telefon raqami kiritilishi shart!"
                }
            )
        user = User.objects.filter(Q(phone=username_phone_email) | Q(email=username_phone_email))
        if not user.exists():
            raise NotFound(detail="User not found")
        attrs['user'] = user.first()
        return attrs

class ForgetPasswordSerializer(serializers.Serializer):
    verify_type = serializers.ChoiceField(choices=['AuthType.via_email', 'AuthType.via_phone'])
    verify_value = serializers.CharField()

    def validate(self, attrs):
        verify_type = attrs.get('verify_type')
        verify_value = attrs.get('verify_value')

        # verify_type ga qarab, qayerdan izlash kerakligini aniqlaymiz
        if verify_type == 'AuthType.via_email':
            user = User.objects.filter(email__iexact=verify_value).first()
        else:  # AuthType.via_phone
            user = User.objects.filter(phone=verify_value).first()

        if not user:
            raise serializers.ValidationError("Bunday foydalanuvchi topilmadi.")
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        verify_type = validated_data['verify_type']
        verify_value = validated_data['verify_value']

        # Eski, tasdiqlanmagan kodlarni o'chirish (ixtiyoriy)
        UserConfirmation.objects.filter(
            user=user,
            verify_type=verify_type,
            is_confirmed=False
        ).delete()

        code = user.create_verify_code(verify_type, verify_value)
        # Bu yerda kodni yuborish uchun email yoki sms jo'natish funksiyasini chaqirishingiz mumkin

        return {'message': 'Tasdiqlash kodi yuborildi.', 'code': code if True else 'hidden'}

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        if hasattr(user, 'profile'):
            raise serializers.ValidationError("Foydalanuvchining profili allaqachon mavjud.")
        return Profile.objects.create(user=user, **validated_data)