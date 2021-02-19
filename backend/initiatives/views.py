from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, mixins, permissions, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters import rest_framework as filters

from .serializers import (
    UserSerializer, OrganizationSerializer, DescriptionDefinitionSerializer, ZoneSerializer,
    CommentSerializer, AreaSerializer, FAQSerializer, FileSerializer, ImageSerializer
)
from .models import Zone, Area, FAQ, DescriptionDefinition, InitiativeType


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


class ZoneViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = ZoneSerializer
    queryset = Zone.objects.all()


class InitiativeTypeApiView(views.APIView):
    def get(self, request):
        return Response([{'id': key , 'name': name} for key, name in InitiativeType.choices])



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


class DescriptionDefinitionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = DescriptionDefinitionSerializer
    queryset = DescriptionDefinition.objects.all().order_by('order')
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('type',)

