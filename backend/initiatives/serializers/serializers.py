from rest_framework import serializers
from django.core.exceptions import ValidationError
from initiatives.models import (
    User, File, StatusInitiative, CompetentService, Organization, Comment,
    CommentStatus, Description, Area, FAQ, Image, DescriptionDefinition,
    Zone, Rejection
)
from behaviors.models import Published
import logging

logger = logging.getLogger(__name__)

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

        organization = Organization.objects.filter(name=organization_name)
        user = super().create(validated_data)
        if not organization:
            organization = Organization(
                name=organization_name,
                number_of_members=number_of_members
            )
            organization.save()
        else:
            raise ValidationError('Organization with this name already exists')

        user.set_password(validated_data['password'])
        user.save()
        user.organizations.add(organization)
        return user

    def validate_organization_name(self, data):
        if Organization.objects.filter(name=data):
            raise ValidationError('Organization with this name already exists')
        return data


class CompetentServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetentService
        fields = ('id', 'name')


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name', 'note')



class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ('id', 'name')


class RejectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rejection
        fields = ('id', 'name', 'note')


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rejection
        fields = ('name',)


class StatusInitiativeSerializerPublishedList(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(publication_status=Published.PUBLISHED).order_by('created')
        return super().to_representation(data)


class StatusInitiativeSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    competent_service = CompetentServiceSerializer()
    class Meta:
        model = StatusInitiative
        list_serializer_class = StatusInitiativeSerializerPublishedList
        fields = (
            'note',
            'created',
            'status',
            'reason_for_rejection',
            'competent_service'
        )
    def get_status(self, obj):
        return obj.status.id

    def get_competent_service(self, obj):
        return obj.competent_service.name if obj.competent_service else None


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file', 'name')


class FileDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file', 'name')
        extra_kwargs = {
            'file': {'read_only': True},
            'name': {'read_only': True},
        }


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', 'name')


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
            'order',
            'id')


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = (
            'question',
            'answer')


class DescriptionDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescriptionDefinition
        fields = (
            'field',
            'title',
            'order')
