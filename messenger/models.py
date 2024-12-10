from django.conf import settings
from django.db import models


class Message(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    def __str__(self):
        return self.text[:10]


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
