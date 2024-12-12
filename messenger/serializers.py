from django.contrib.auth import get_user_model
from rest_framework import serializers

from messenger.models import Message, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
        )


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "id",
            "text",
            "created_at",
            "user",
        )
        # DON'T USE fields = "__all__" !!!!!!!!!!!!!!!!!!!!!!!!!


class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "id",
            "text_preview",
            "created_at",
            "user",
        )


class MessageDetailSerializer(MessageSerializer):
    user = UserSerializer(read_only=True)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")
