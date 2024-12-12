from django.urls import path, include
from rest_framework import routers

from messenger.views import MessageViewSet, TagViewSet

app_name = "messenger"

router = routers.DefaultRouter()
router.register("messages", MessageViewSet, basename="messages")
router.register("tags", TagViewSet, basename="tags")

urlpatterns = [path("", include(router.urls))]
