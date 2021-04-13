from rest_framework import serializers

from initiatives.models import Initiative

from initiatives.serializers import (
    AreaSerializer, ImageSerializer, StatusInitiativeSerializer, FileDetailsSerializer, DescriptionSerializers, CommentSerializer
)
from initiatives.models import CommentStatus

from drf_writable_nested.serializers import WritableNestedModelSerializer

class InitiativeListSerializer(serializers.ModelSerializer):
    area = AreaSerializer()
    author = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField(required=False)
    cover_image = ImageSerializer(required=False)
    has_voted = serializers.SerializerMethodField()
    class Meta:
        model = Initiative
        fields = (
            'type',
            'id',
            'title',
            'location',
            'created',
            'cover_image',
            'area',
            'comment_count',
            'vote_count',
            'status',
            'author',
            'description',
            'has_voted')

    def get_author(self, obj):
        return obj.author.username

    # TODO
    def get_description(self, obj):
        return '\n'.join(obj.descriptions.order_by('order').values_list('content', flat=True))[:100]

    def get_has_voted(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user.is_authenticated:
                vote = obj.votes.filter(author=user)
                if vote:
                    return True

        return False


class InitiativeDetailsSerializer(WritableNestedModelSerializer):
    statuses = StatusInitiativeSerializer(source='initiative_statuses', many=True, required=False)
    uploaded_files = FileDetailsSerializer(source='files', many=True, required=False)
    author = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    descriptions = DescriptionSerializers(many=True, required=False)
    cover_image = ImageSerializer(required=False, allow_null=True)
    cover_image_after = ImageSerializer(required=False)
    has_voted = serializers.SerializerMethodField()

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
            'descriptions',
            'is_draft',
            'has_voted')
        extra_kwargs = {
            'author': {'read_only': False},
            'cover_image_after': {'read_only': True},
            'statuses': {'read_only': True},
            'created': {'read_only': True},
            'comments': {'read_only': True},
        }

    def get_area(self, obj):
        return AreaSerializer(obj.area).data

    def get_comments(self, obj):
        qs = obj.initiative_comments.filter(status=CommentStatus.PUBLISHED)
        serializer = CommentSerializer(instance=qs, many=True)
        return serializer.data

    def get_author(self, obj):
        return obj.author.username

    def get_has_voted(self, obj):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            if user.is_authenticated:
                vote = obj.votes.filter(author=user)
                if vote:
                    return True

        return False
