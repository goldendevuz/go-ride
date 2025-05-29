from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Appointment, Reason, Review, Rate, ReviewLike

User = get_user_model()

class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)  # Doctor creation is not in this serializer
    status = serializers.ChoiceField(choices=Appointment.Status.choices, default=Appointment.Status.PENDING)
    service = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)

    class Meta:
        model = Appointment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set service queryset to active services only
        self.fields['service'].queryset = self.Meta.model._meta.get_field('service').related_model.objects.filter(is_active=True)

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    appointment = serializers.PrimaryKeyRelatedField(queryset=Appointment.objects.all())

    class Meta:
        model = Review
        fields = '__all__'

    def validate_text(self, value):
        if len(value) < 10:
            raise serializers.ValidationError('Text is too short (min 10 characters).')
        if len(value) > 1000:
            raise serializers.ValidationError('Text is too long (max 1000 characters).')
        return value

class RateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all())

    class Meta:
        model = Rate
        fields = '__all__'

class ReviewLikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all())

    class Meta:
        model = ReviewLike
        fields = '__all__'

    def validate(self, data):
        user = data.get('user')
        review = data.get('review')
        if ReviewLike.objects.filter(user=user, review=review).exists():
            raise serializers.ValidationError("You have already liked this review.")
        return data