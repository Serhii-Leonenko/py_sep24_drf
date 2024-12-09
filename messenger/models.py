from django.db import models


class Message(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:10]


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
