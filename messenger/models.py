from django.conf import settings
from django.db import models

from base.models import UUIDBaseModel
from messenger.utils import message_image_file_path


class Tag(UUIDBaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Message(UUIDBaseModel):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="messages")
    image = models.ImageField(null=True, blank=True, upload_to=message_image_file_path)

    @property
    def text_preview(self):
        if len(self.text) < 50:
            return str(self)

        return f"{self.text[:50:]}..."

    def __str__(self):
        return self.text[:20]


class Like(UUIDBaseModel):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("message", "user")
