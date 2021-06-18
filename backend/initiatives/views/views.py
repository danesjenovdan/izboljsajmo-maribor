from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import viewsets, mixins, permissions, status, views, authentication, exceptions, pagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_social_oauth2.views import TokenView
from django_filters import rest_framework as filters
from rest_framework import filters as s_filters
from behaviors.behaviors import Published

from initiatives.serializers import (
    UserSerializer, OrganizationSerializer, DescriptionDefinitionSerializer, ZoneSerializer,
    CommentSerializer, AreaSerializer, FAQSerializer, FileSerializer, ImageSerializer,
    InitiativeDetailsSerializer, InitiativeListSerializer, AddressSerializer
)
from initiatives.models import (
    Zone, Area, FAQ, DescriptionDefinition, InitiativeType, Initiative, Reviwers, Vote, RestorePassword,
    ConfirmEmail, User, NotificationType, Notification, Address
)
from initiatives.permissions import IsOwnerOrReadOnly, IsVerified, IsBlocked
from initiatives.tasks import send_email_task

from datetime import datetime

import logging
import json
logger = logging.getLogger(__name__)

class TokenView(TokenView):
    def create_token_response(self, request):
        """
        workaround for login with email or username
        """
        username = request.POST.pop('username', None)
        if username:
            username = get_user_model().objects.filter(Q(email=username[0])|Q(username=username[0])).values_list('username', flat=True).last()
            body = json.loads(request._body)
            body['username'] = username
            request._body = bytes(json.dumps(body), 'utf-8')
        return super(TokenView, self).create_token_response(request)

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
        permission_classes=[permissions.IsAuthenticated, IsVerified])
    def my_initiatives(self, request):
        return Response(UserSerializer(request.user).data)


class OrganizationViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = OrganizationSerializer


class AddressPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'per_page'
    max_page_size = 20


class AddressViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = AddressSerializer
    filter_backends = (s_filters.SearchFilter,)
    search_fields = ['name']
    queryset = Address.objects.all().order_by('name')
    pagination_class = AddressPagination


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
    permission_classes = [permissions.IsAuthenticated, IsVerified, IsBlocked]


class ImagesViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin):
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [permissions.IsAuthenticated, IsVerified, IsBlocked]


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
    no_zone = filters.BooleanFilter(field_name='zone', lookup_expr='isnull')
    statuses = filters.CharFilter(method='filter_statuses')

    def filter_statuses(self, queryset, name, value):
        return queryset.filter(initiative_statuses__status__name=value)


    class Meta:
        model = Initiative
        fields = ['zone', 'area', 'type', 'no_zone', 'statuses']


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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.exclude(
            is_draft=True
        ).exclude(
            statuses__name='Zavrnjeno'
        ).filter(
            initiative_statuses__publication_status=Published.PUBLISHED
        ).distinct('id').order_by('id', 'created')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    def get_serializer_class(self):
        if self.action == 'list':
            return InitiativeListSerializer
        return InitiativeDetailsSerializer

    def send_emails(self, instance):
        users = User.objects.filter(role=Reviwers.SUPER_ADMIN)
        for user in users:
            Notification(
                initiative=instance,
                type=NotificationType.NEW,
                for_user=user
            ).save()
        if instance.area:
            Notification(
                initiative=instance,
                type=NotificationType.NEW,
                for_area=instance.area
            ).save()
        send_email_task.delay(
            f'#{instance.id} {instance.title}',
            settings.LOG_EMAIL,
            'emails/new_initiative_log.html',
            {
                'name': instance.title,
                'id': instance.id
            }
        )
        if instance.type == InitiativeType.BOTHERS_ME:
            template = 'emails/bothers.html'
        elif instance.type == InitiativeType.HAVE_IDEA:
            template = 'emails/idea.html'
        elif instance.type == InitiativeType.INTERESTED_IN:
            template = 'emails/interested.html'
        send_email_task.delay(
            f'#{instance.id} {instance.title}',
            instance.author.email,
            template,
            {}
        )

    def create(self, request, *args, **kwargs):
        area = request.data.get('area', None)
        if area:
            area = Area.objects.get(id=area)
        for i, desctription in enumerate(request.data.get('descriptions', [])):
            request.data['descriptions'][i]['order'] = i + 1
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(author=request.user, area=area)
        headers = self.get_success_headers(serializer.data)
        instance = serializer.instance
        if not instance.is_draft:
            self.send_emails(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        data = request.data
        area = data.get('area', None)
        if area:
            area = Area.objects.get(id=area)
        for i, desctription in enumerate(data.get('descriptions', [])):
            data['descriptions'][i]['order'] = i + 1

        instance = self.get_object()
        is_draft = instance.is_draft

        if is_draft == True and data['is_draft'] == False:
            instance.created=datetime.now()


        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(area=area)

        if is_draft == True and data['is_draft'] == False:
            self.send_emails(serializer.instance)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

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
        methods=['post', 'delete'],
        detail=True,
        url_path='vote',
        url_name='vote',
        permission_classes=[permissions.IsAuthenticated,])
    def votes(self, request, pk=None):
        logger.warning(request.method)
        if request.method == 'POST':
            logger.warning(pk)
            initiative = get_object_or_404(Initiative, pk=pk)
            ex_vote = Vote.objects.filter(author=request.user, initiative=initiative)
            if ex_vote:
                return Response({'detail': _('You already voted for this initiative.')}, status.HTTP_409_CONFLICT)
            else:
                Vote(author=request.user, initiative=initiative).save()
                return Response({'detail': 'done'})
        elif request.method == 'DELETE':
            initiative = get_object_or_404(Initiative, pk=pk)
            ex_vote = Vote.objects.filter(author=request.user, initiative=initiative)
            if ex_vote:
                ex_vote.delete()
                return Response({'detail': 'deleted'}, status.HTTP_204_NO_CONTENT)
            else:
                return Response({'detail': _('You need to vote first.')}, status.HTTP_409_CONFLICT)
        else:
            raise exceptions.MethodNotAllowed(request.method)

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


class RestorePasswordApiView(views.APIView):
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        data = request.data
        user = get_object_or_404(User, email=data.get('email', ''))
        RestorePassword(user=user).save()
        return Response({'status': _('Email will be send.')}, status=status.HTTP_201_CREATED)

    def patch(self, request, key):
        restore_password = get_object_or_404(RestorePassword, key=key)
        password = request.data.get('new_password')
        try:
            validate_password(password, user=None, password_validators=None)
        except ValidationError as e:
            return Response({'detail': e}, status=status.HTTP_409_CONFLICT)
        user = restore_password.user
        user.set_password(password)
        user.save()
        restore_password.delete()
        send_email_task.delay(
            _('Sprememba gesla za dostop do platforme Izboljšajmo Maribor'),
            user.email,
            'emails/restore_password_done.html',
            {
            }
        )
        return Response({'status': _('Password has been set.')})


class ConfirmEmailApiView(views.APIView):
    permission_classes = []
    authentication_classes = []
    def get(self, request, key):
        confirm_email = get_object_or_404(ConfirmEmail, key=key)
        user = confirm_email.user
        user.email_confirmed = True
        user.save()
        confirm_email.delete()
        return Response({'status': _('Email confirmed.')})
