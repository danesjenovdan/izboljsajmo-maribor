from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import (
    UserSerializer, OrganizationSerializer,
    CommentSerializer, AreaSerializer,
    FAQSerializer, FileSerializer, ImageSerializer
)
from .models import Zone, Area, FAQ


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserSerializer


class OrganizationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = OrganizationSerializer


class AreaViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = AreaSerializer
    queryset = Area.objects.all()


class FilesViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin):
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [permissions.IsAuthenticated,]


class ImagesViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin):
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [permissions.IsAuthenticated,]


class FAQViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all().order_by('order')
