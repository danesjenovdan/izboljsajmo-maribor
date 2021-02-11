from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    UserSerializer, InitiativeDetailsSerializer, OrganizationSerializer,
    CommentSerializer, InitiativeListSerializer
)
from .models import Initiative, Zone, Area


class UserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserSerializer


class OrganizationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = OrganizationSerializer


class InitiativeViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    serializer_class = InitiativeDetailsSerializer
    queryset = Initiative.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return InitiativeListSerializer
        return InitiativeDetailsSerializer


    def create(self, request, *args, **kwargs):
        area = request.data['area']
        area = Area.objects.get(id=area)
        for i, desctription in enumerate(request.data['descriptions']):
            request.data['descriptions'][i]['order'] = i + 1
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # TODO get zone from location
        zone = Zone.objects.first()

        serializer.save(zone=zone, author=request.user, area=area)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(
        methods=['post'],
        detail=True,
        url_path='comments',
        url_name='comments',
        permission_classes=[permissions.IsAuthenticated,])
    def comments(self, request, pk=None):
        initiative = get_object_or_404(Initiative, pk=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save(author = request.user, initiative = initiative)
            return Response(serializer.data)


