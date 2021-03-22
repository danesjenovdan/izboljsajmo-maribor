from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet, OrganizationViewSet, AreaViewSet, FAQViewSet, FilesViewSet, InitiativeViewSet,
    ImagesViewSet, DescriptionDefinitionViewSet, ZoneViewSet, InitiativeTypeApiView, MoveResponsibilityApiView,
    ArchiveApiView, RejectionViewSet
)

from about.views import AboutViewSet


app_name = 'initiatives'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='User')
router.register(r'organizations', OrganizationViewSet, basename='Organization')
router.register(r'areas', AreaViewSet, basename='Area')
router.register(r'zones', ZoneViewSet, basename='Zone')
router.register(r'about', AboutViewSet, basename='About')
router.register(r'faq', FAQViewSet, basename='FAQ')
router.register(r'images', ImagesViewSet, basename='Image')
router.register(r'files', FilesViewSet, basename='File')
router.register(r'description-definitions', DescriptionDefinitionViewSet, basename='DescriptionDefinition')
router.register(r'initiatives', InitiativeViewSet, basename='Initiative')
router.register(r'rejections', RejectionViewSet, basename='Rejections')



urlpatterns = [
    path('', include((router.urls, 'initiatives'))),
    path('initiative-types/', InitiativeTypeApiView.as_view()),
    path('move-responsibility/<str:label>/<int:pk>/<str:next>/', MoveResponsibilityApiView.as_view(), name='move-responsibility'),
    path('archive/<str:label>/<int:pk>/', ArchiveApiView.as_view(), name='archive'),
]
