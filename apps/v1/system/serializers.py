from adrf.serializers import ModelSerializer
from django.utils import timezone
from rest_framework import serializers

from apps.v1.system.models import (
    Notification,
    NotificationSetting,
    Payment,
)

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

    def validate_send_at(self, value):
        if timezone.is_naive(value):
            value = timezone.make_aware(value)

        if value < timezone.now():
            raise serializers.ValidationError("Notification date and time cannot be in the past.")
        return value

class NotificationSettingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # faqat o'qish uchun

    class Meta:
        model = NotificationSetting
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # faqat o'qish uchun
    reviewed_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['reviewed_by'] = request.user
        return super().update(instance, validated_data)