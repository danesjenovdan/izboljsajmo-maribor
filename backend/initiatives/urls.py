from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter

from .views import UserViewSet, InitiativeViewSet


app_name = 'initiatives'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='User')
router.register(r'initiatives', InitiativeViewSet, basename='Initiative')


urlpatterns = [
    path('', include((router.urls, 'initiatives'))),
]
