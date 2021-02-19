from django.shortcuts import render
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework import filters as s_filters

from .serializers import (
    InitiativeDetailsSerializer, InitiativeListSerializer
)
from .models import Initiative
from .permissions import IsOwnerOrReadOnly

from initiatives.models import Area, Zone

class InitiativeViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin):
    permission_classes = [IsOwnerOrReadOnly, ]
    serializer_class = InitiativeDetailsSerializer
    queryset = Initiative.objects.all()
    filter_backends = (filters.DjangoFilterBackend, s_filters.SearchFilter)
    filterset_fields = ('zone', 'area', 'type')
    search_fields = ['title', 'zone__name', 'area__name']


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

    @action(
        methods=['get'],
        detail=False,
        url_path='my',
        url_name='my',
        permission_classes=[permissions.IsAuthenticated,])
    def my_initiatives(self, request, pk=None):
        initiatives = Initiative.objects.filter(author=request.user)
        drafts = initiatives.filter(is_draft=True)
        published = initiatives.filter(is_draft=False)
        draft_serializer = InitiativeListSerializer(drafts, many=True)
        serializer = InitiativeListSerializer(published, many=True)
        return Response({'drafts': draft_serializer.data, 'published': serializer.data})
