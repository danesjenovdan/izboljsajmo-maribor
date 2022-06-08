from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.shortcuts import render
from django.views import View
from django.utils.translation import gettext as _
from django.http import HttpResponse

from rest_framework import viewsets, mixins, permissions, views, authentication
from rest_framework.decorators import action
from rest_framework.response import Response

from datetime import datetime

from initiatives.serializers import RejectionSerializer
from initiatives.models import Initiative, Reviwers, Rejection

import csv

DETE_FORMAT = '%d.%m.%Y'

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


class ExportApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated,]
    authentication_classes = [authentication.SessionAuthentication,]
    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.writer(response)
        #writer.writerow([_('ID'), _('Created'), _('Is archived'), _('Title'), _('Author'), _('Last status'), _('Zone'), _('Address'), _('Area'), _('Description'), _('Status'), _('Status date'), _('Status note')])
        writer.writerow([_('ID'), _('Created'), _('Is archived'), _('Title'), _('Author'), _('Last status'), _('Zone'), _('Address'), _('Area'), _('Description')])
        initiatives = Initiative.objects.filter(is_draft=False).order_by('created')
        for initiative in initiatives:
            #statuses = initiative.initiative_statuses.all().order_by('created')
            #if statuses:
            #    for status in statuses:
            #        writer.writerow(self.get_initiative_row(initiative) + self.get_status_row(status))
            #
            #else:
            writer.writerow(self.get_initiative_row(initiative) + [''] * 3)
        return response

    def get_initiative_row(self, initiative):
        return  [
            initiative.id,
            initiative.created.strftime(DETE_FORMAT),
            _('Archived') if initiative.is_archived() else '',
            initiative.title,
            initiative.author.username,
            initiative.status(),
            initiative.zone,
            initiative.address,
            initiative.area,
            ' '.join(initiative.descriptions.values_list('content', flat=True))
        ]

    def get_status_row(self, status):
        return [
            status.status.name,
            status.created.strftime(DETE_FORMAT),
            status.note,
        ]


class RejectionViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin):
    permission_classes = []
    serializer_class = RejectionSerializer
    queryset = Rejection.objects.all()


class PrintInitiativesView(View):
    def get(self, request, pk):
        initiatives = Initiative.objects.filter(pk=pk)
        return render(request, 'print/initiatives.html', {'initiatives': initiatives})
