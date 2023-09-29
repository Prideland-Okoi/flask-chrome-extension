# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScreenRecordingViewSet, SavedSharedVideoViewSet

router = DefaultRouter()
router.register(r'screen-recordings', ScreenRecordingViewSet)
router.register(r'saved-shared-videos', SavedSharedVideoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
