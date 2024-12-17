from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.serializers import UserSerializer
from messenger.models import Message, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "id",
            "text",
            "created_at",
            "user",
            "tags",
            "image"
        )
        read_only_fields = ("id", "user", "created_at")
        # DON'T USE fields = "__all__" !!!!!!!!!!!!!!!!!!!!!!!!!


class MessageListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        read_only=True
    )
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "text_preview",
            "created_at",
            "user",
            "tags",
            "image",
            "likes_count"
        )
        read_only_fields = fields


class MessageDetailSerializer(MessageSerializer):
    user = UserSerializer(read_only=True)
