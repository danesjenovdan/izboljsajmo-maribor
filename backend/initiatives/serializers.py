from rest_framework import serializers
from .models import User, Initiative, File, StatusInitiative

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'phone_number')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class StatusInitiativeSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    competent_service = serializers.SerializerMethodField()
    class Meta:
        model = StatusInitiative
        fields = (
            'note',
            'created',
            'status',
            'reason_for_rejection',
            'competent_service'
        )
    def get_status(self, obj):
        return obj.status.name

    def get_competent_service(self, obj):
        return obj.competent_service.name if obj.competent_service else None


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('file', 'name')


class InitiativeDetailsSerializer(serializers.ModelSerializer):
    statuses = StatusInitiativeSerializer(source='initiative_statuses', many=True)
    uploaded_files = FileSerializer(source='files', many=True)
    class Meta:
        model = Initiative
        fields = (
            'id',
            'type',
            'title',
            'area',
            'location',
            'cover_image',
            'cover_image_after',
            'uploaded_files',
            'statuses')
