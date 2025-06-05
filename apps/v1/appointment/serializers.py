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
        exclude = ['user']

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
    appointment = serializers.PrimaryKeyRelatedField(queryset=Appointment.objects.all())

    class Meta:
        model = Review
        exclude = ['user']

    def validate_text(self, value):
        if len(value) < 10:
            raise serializers.ValidationError('Text is too short (min 10 characters).')
        if len(value) > 1000:
            raise serializers.ValidationError('Text is too long (max 1000 characters).')
        return value

class RateSerializer(serializers.ModelSerializer):
    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all())

    class Meta:
        model = Rate
        exclude = ['user']

class ReviewLikeSerializer(serializers.ModelSerializer):
    review = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all())

    class Meta:
        model = ReviewLike
        exclude = ['user']

    def validate(self, data):
        user = data.get('user')
        review = data.get('review')
        if ReviewLike.objects.filter(user=user, review=review).exists():
            raise serializers.ValidationError("You have already liked this review.")
        return data