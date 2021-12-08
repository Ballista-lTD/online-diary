from django.urls import path, include
from rest_framework.routers import DefaultRouter

from home.views import EventApiViewSet


# Setup the URLs and include login URLs for the browsable API.
router = DefaultRouter()
router.register('event', EventApiViewSet)
urlpatterns = [
    path(r'', include(router.urls)),
]
