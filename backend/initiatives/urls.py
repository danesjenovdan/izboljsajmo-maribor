from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet, InitiativeViewSet, OrganizationViewSet, AreaViewSet, FAQViewSet, FilesViewSet,
    ImagesViewSet
)

from about.views import AboutViewSet


app_name = 'initiatives'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='User')
router.register(r'organizations', OrganizationViewSet, basename='Organization')
router.register(r'initiatives', InitiativeViewSet, basename='Initiative')
router.register(r'areas', AreaViewSet, basename='Area')
router.register(r'about', AboutViewSet, basename='About')
router.register(r'faq', FAQViewSet, basename='FAQ')
router.register(r'images', ImagesViewSet, basename='Image')
router.register(r'files', FilesViewSet, basename='File')



urlpatterns = [
    path('', include((router.urls, 'initiatives'))),
]
