from rest_framework import serializers

from apps.v1.clinic.models import Specialty, Hospital
from apps.v1.doctor.models import Doctor, Favorite, History, SecuritySetting, WorkingHour

class DoctorSerializer(serializers.ModelSerializer):
    specialty = serializers.PrimaryKeyRelatedField(
        queryset=Specialty.objects.all(),
        required=True,
        allow_null=False
    )
    hospital = serializers.PrimaryKeyRelatedField(
        queryset=Hospital.objects.all(),
        required=True,
        allow_null=False
    )
    about = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        read_only_fields = ['id']

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']

class SecuritySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecuritySetting
        fields = '__all__'
        read_only_fields = ['id']

class WorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingHour
        fields = '__all__'
        read_only_fields = ['id']

    def validate(self, data):
        start = data.get('start_time')
        end = data.get('end_time')
        if start and end and start >= end:
            raise serializers.ValidationError("Ish boshlanish vaqti tugash vaqtidan oldin bo'lishi kerak.")
        return data