from rest_framework import serializers
from .models import User, Initiative, File, StatusInitiative, CompetentService, Organization

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

class OrganizationSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(required=False)
    number_of_members = serializers.IntegerField(required=False)
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
            'phone_number',
            'number_of_members',
            'organization_name')
        extra_kwargs = {
            'number_of_members': {'required': False},
            'organization_name': {'required': False},
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        organization_name = validated_data.pop('organization_name', None)
        number_of_members = validated_data.pop('number_of_members', None)

        user = super().create(validated_data)

        organization = Organization.objects.filter(name=organization_name)
        if not organization:
            organization = Organization(
                name=organization_name,
                number_of_members=number_of_members
            )
            organization.save()
        else:
            organization = organization[0]

        user.set_password(validated_data['password'])
        user.save()
        user.organizations.add(organization)
        return user


class GetCompetentService(serializers.ModelSerializer):
    class Meta:
        model = CompetentService
        fields = ('id', 'name')


class StatusInitiativeSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    competent_service = GetCompetentService()
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
    author = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    class Meta:
        model = Initiative
        fields = (
            'id',
            'type',
            'title',
            'area',
            'location',
            'author',
            'cover_image',
            'cover_image_after',
            'uploaded_files',
            'statuses',
            'created',
            'address')

    def get_author(self, obj):
        return obj.author.username

    def get_area(self, obj):
        return obj.area.name
