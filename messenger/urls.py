from django.urls import path

from messenger.views import MessageListView, TagListView

app_name = "messenger"

urlpatterns = [
    path("messages/", MessageListView.as_view(), name="message-list"),
    path("tags/", TagListView.as_view(), name="tag-list")
]
