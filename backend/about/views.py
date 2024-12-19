from rest_framework import mixins, permissions, viewsets

from .models import About
from .serializers import AboutSerializer


class AboutViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = AboutSerializer
    queryset = About.objects.all().order_by("order")
