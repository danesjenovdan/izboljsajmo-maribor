from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from rest_framework import viewsets, mixins, permissions, status, views, authentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters import rest_framework as filters
from rest_framework import filters as s_filters

from initiatives.serializers import (
    UserSerializer, OrganizationSerializer, DescriptionDefinitionSerializer, ZoneSerializer,
    CommentSerializer, AreaSerializer, FAQSerializer, FileSerializer, ImageSerializer,
    InitiativeDetailsSerializer, InitiativeListSerializer
)
from initiatives.models import Zone, Area, FAQ, DescriptionDefinition, InitiativeType, Initiative, Reviwers, Vote

from initiatives.permissions import IsOwnerOrReadOnly


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = UserSerializer

    @action(
        methods=['get'],
        detail=False,
        url_path='me',
        url_name='me',
        permission_classes=[permissions.IsAuthenticated,])
    def my_initiatives(self, request):
        return Response(UserSerializer(request.user).data)


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


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class InitiativeFilterSet(filters.FilterSet):
    type = CharInFilter(field_name='type', lookup_expr='in')
    zone = CharInFilter(field_name='zone', lookup_expr='in')
    area = CharInFilter(field_name='area', lookup_expr='in')

    class Meta:
        model = Initiative
        fields = ['zone', 'area', 'type']


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
    filterset_class = InitiativeFilterSet
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
        methods=['post'],
        detail=True,
        url_path='vote',
        url_name='vote',
        permission_classes=[permissions.IsAuthenticated,])
    def votes(self, request, pk=None):
        initiative = get_object_or_404(Initiative, pk=pk)
        ex_vote = Vote.objects.filter(author=request.user, initiative=initiative)
        if ex_vote:
            return Response({'detail': _('You already voted for this initiative.')}, 409)
        else:
            Vote(author=request.user, initiative=initiative).save()
            return Response({'detail': 'done'})

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
        draft_serializer = InitiativeListSerializer(drafts, context = {'request':request}, many=True)
        serializer = InitiativeListSerializer(published, context = {'request':request}, many=True)
        return Response({'drafts': draft_serializer.data, 'published': serializer.data})

