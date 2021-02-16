from rest_framework import viewsets, mixins, permissions

from .serializers import AboutSerializer
from .models import  About


class AboutViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = AboutSerializer
    queryset = About.objects.all().order_by('order')
