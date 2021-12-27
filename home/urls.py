from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EventApiViewSet, ReportApiViewSet

router = DefaultRouter()
router.register('', EventApiViewSet)
router.register('report', ReportApiViewSet)

urlpatterns = [
    path(r'', include(router.urls))
]
