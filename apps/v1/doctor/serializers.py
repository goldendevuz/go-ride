from rest_framework import serializers
from apps.v1.doctor.models import Doctor, Favorite, History, SecuritySetting, WorkingHour

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialty', 'hospital', 'rating', 'review_count', 'about']
        read_only_fields = ['id', 'rating', 'review_count']

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'doctor']
        read_only_fields = ['id']

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'doctor', 'action', 'timestamp']
        read_only_fields = ['id', 'timestamp']

class SecuritySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecuritySetting
        fields = ['id', 'user', 'remember_me', 'face_id', 'biometric_id']
        read_only_fields = ['id']

class WorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHour
        fields = ['id', 'doctor', 'day_of_week', 'start_time', 'end_time']
        read_only_fields = ['id']

    def validate(self, data):
        start = data.get('start_time')
        end = data.get('end_time')
        if start and end and start >= end:
            raise serializers.ValidationError("Ish boshlanish vaqti tugash vaqtidan oldin bo'lishi kerak.")
        return data