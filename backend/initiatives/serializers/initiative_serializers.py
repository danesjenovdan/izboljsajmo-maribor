from itertools import groupby

from behaviors.models import Published
from drf_writable_nested.serializers import WritableNestedModelSerializer
from initiatives.models import CommentStatus, Initiative
from initiatives.serializers import (
    AreaSerializer,
    CommentSerializer,
    DescriptionSerializers,
    FileDetailsSerializer,
    ImageSerializer,
    StatusInitiativeSerializer,
)
from rest_framework import serializers


class InitiativeListSerializer(serializers.ModelSerializer):
    area = AreaSerializer()
    author = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField(required=False)
    cover_image = ImageSerializer(required=False)
    has_voted = serializers.SerializerMethodField()

    class Meta:
        model = Initiative
        fields = (
            "type",
            "id",
            "title",
            "location",
            "created",
            "cover_image",
            "area",
            "comment_count",
            "vote_count",
            "is_social_inovative_idea",
            "status",
            "author",
            "description",
            "has_voted",
        )

    def get_author(self, obj):
        return obj.author.username

    def get_description(self, obj):
        return (
            " ".join(
                " ".join(
                    obj.descriptions.order_by("order").values_list("content", flat=True)
                )[:100].split(" ")[:-1]
            )
            + "..."
        )

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
    statuses = serializers.SerializerMethodField()
    uploaded_files = FileDetailsSerializer(source="files", many=True, required=False)
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
            "id",
            "type",
            "title",
            "area",
            "location",
            "author",
            "cover_image",
            "cover_image_after",
            "uploaded_files",
            "statuses",
            "created",
            "address",
            "comments",
            "descriptions",
            "is_draft",
            "is_social_inovative_idea",
            "has_voted",
        )
        extra_kwargs = {
            "author": {"read_only": False},
            "cover_image_after": {"read_only": True},
            "statuses": {"read_only": True},
            "created": {"read_only": True},
            "comments": {"read_only": True},
        }

    def get_statuses(self, obj):
        output = []
        statuses = obj.initiative_statuses.filter(
            publication_status=Published.PUBLISHED
        ).order_by("status")
        for status, items in groupby(statuses, key=lambda x: x.status.name):
            responses = sorted(
                [StatusInitiativeSerializer(item).data for item in items],
                key=lambda i: i["created"],
            )
            output.append(
                {
                    "status": status,
                    "created": responses[0]["created"],
                    "responses": responses,
                }
            )
        return output

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
