from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet, InitiativeViewSet, OrganizationViewSet, AreaViewSet, AboutViewSet
)


app_name = 'initiatives'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='User')
router.register(r'organizations', OrganizationViewSet, basename='Organization')
router.register(r'initiatives', InitiativeViewSet, basename='Initiative')
router.register(r'areas', AreaViewSet, basename='Area')
router.register(r'about', AboutViewSet, basename='About')



urlpatterns = [
    path('', include((router.urls, 'initiatives'))),
]
