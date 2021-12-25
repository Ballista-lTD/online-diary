from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GroupApiViewSet, promote

router = DefaultRouter()

router.register('group', GroupApiViewSet)

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'promote/', promote)
]
