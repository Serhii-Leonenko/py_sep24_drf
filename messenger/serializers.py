from rest_framework import serializers

from messenger.models import Message, Tag


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "id",
            "text",
            "created_at",
            "user"
        )


class MessageListSerializer(MessageSerializer):
    user = serializers.CharField(source="user.username") # username instead of id

    class Meta:
        model = Message
        fields = (
            "id",
            "text",
            "created_at",
            "user"
        )
        read_only_fields = fields


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "name"
        )
