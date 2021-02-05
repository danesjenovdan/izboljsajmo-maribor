from django.shortcuts import render

from rest_framework import viewsets, mixins, permissions

from .serializers import UserSerializer, InitiativeDetailsSerializer, OrganizationSerializer
from .models import Initiative


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserSerializer


class OrganizationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = OrganizationSerializer


class InitiativeViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = InitiativeDetailsSerializer
    queryset = Initiative.objects.all()
