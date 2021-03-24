from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from rest_framework import viewsets, mixins, permissions, views, authentication
from rest_framework.decorators import action
from rest_framework.response import Response

from datetime import datetime

from initiatives.serializers import RejectionSerializer
from initiatives.models import Initiative, Reviwers, Rejection


class MoveResponsibilityApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated,]
    authentication_classes = [authentication.SessionAuthentication,]
    def get(self, request, pk, label, next):
        initiative = Initiative.objects.get(pk=pk)
        initiative.reviewer = next
        initiative.save()
        return redirect('admin:%s_%s_changelist' % (initiative._meta.app_label,  label))


class ArchiveApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated,]
    authentication_classes = [authentication.SessionAuthentication,]
    def get(self, request, pk, label):
        initiative = Initiative.objects.get(pk=pk)
        initiative.archived = datetime.now()
        initiative.save()
        return redirect('admin:%s_%s_changelist' % (initiative._meta.app_label,  label))


class RejectionViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin):
    permission_classes = []
    serializer_class = RejectionSerializer
    queryset = Rejection.objects.all()
