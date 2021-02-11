from rest_framework import serializers
from .models import (
    User, Initiative, File, StatusInitiative, CompetentService, Organization, Comment,
    CommentStatus, Description, Area, About
)

from drf_writable_nested.serializers import WritableNestedModelSerializer


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


class CompetentServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetentService
        fields = ('id', 'name')


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name')


class StatusInitiativeSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    competent_service = CompetentServiceSerializer()
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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = (
            'content',
            'author',
            'created')
        extra_kwargs = {
            'author': {'read_only': False},
            'created': {'read_only': True},
        }

    def get_author(self, obj):
        return obj.author.username


class DescriptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Description
        fields = (
            'content',
            'field',
            'title',
            'order')


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = (
            'type',
            'content',
            'image',
            'url')



class InitiativeListSerializer(serializers.ModelSerializer):
    area = AreaSerializer()
    author = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    class Meta:
        model = Initiative
        fields = (
            'type',
            'title',
            'location',
            'created',
            'cover_image',
            'area',
            'comment_count',
            'vote_count',
            'status',
            'author',
            'description')

    def get_author(self, obj):
        return obj.author.username

    # TODO
    def get_description(self, obj):
        return 'Dummy text'

class InitiativeDetailsSerializer(WritableNestedModelSerializer):
    statuses = StatusInitiativeSerializer(source='initiative_statuses', many=True, required=False)
    uploaded_files = FileSerializer(source='files', many=True, required=False)
    author = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    descriptions = DescriptionSerializers(many=True)
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
            'address',
            'comments',
            'descriptions')
        extra_kwargs = {
            'author': {'read_only': False},
            'cover_image_after': {'read_only': True},
            'statuses': {'read_only': True},
            'created': {'read_only': True},
            'comments': {'read_only': True},
        }

    def get_author(self, obj):
        return obj.author.username

    def get_area(self, obj):
        return AreaSerializer(obj.area).data

    def get_comments(self, obj):
        qs = Comment.objects.filter(initiative=obj, status=CommentStatus.PUBLISHED)
        serializer = CommentSerializer(instance=qs, many=True)
        return serializer.data




