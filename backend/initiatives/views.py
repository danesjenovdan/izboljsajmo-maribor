from django.shortcuts import render

from rest_framework import viewsets, mixins, permissions

from .serializers import UserSerializer


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserSerializer

