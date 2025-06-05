from datetime import datetime
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Appointment, Reason, Review, Rate, ReviewLike

User = get_user_model()

class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, attrs):
        date = attrs.get('date')
        time = attrs.get('time')

        if date and time:
            appointment_datetime = datetime.combine(date, time)

            # Naive datetime ni timezone-aware ga aylantiramiz
            if timezone.is_naive(appointment_datetime):
                appointment_datetime = timezone.make_aware(appointment_datetime)

            if appointment_datetime < timezone.now():
                raise serializers.ValidationError("Appointment date and time cannot be in the past.")

        return attrs

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