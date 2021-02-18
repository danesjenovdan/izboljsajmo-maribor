from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter

from .views import InitiativeViewSet


app_name = 'initiative'

router = DefaultRouter()
router.register(r'initiatives', InitiativeViewSet, basename='Initiative')



urlpatterns = [
    path('', include((router.urls, 'initiative'))),
]
