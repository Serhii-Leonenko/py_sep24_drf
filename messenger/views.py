from django.db.models import Count, Prefetch
from django.shortcuts import render
from django.template.context_processors import request
from django.utils.archive import extract
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from drf_spectacular.utils import extend_schema
from jsonschema.validators import extend
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from base.mixins import BaseViewMethodsMixin
from messenger.filters import MessageFilter
from messenger.models import Like, Message, Tag
from messenger.permissions import IsOwner
from messenger.serializers import (MessageDetailSerializer,
                                   MessageListSerializer, MessageSerializer,
                                   TagSerializer)

from django.views.decorators.cache import cache_page


# VIOLATING SRP !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# @api_view(["GET", "POST"])
# def message_list(request: Request) -> Response:
#     if request.method == "GET":
#         messages = Message.objects.all()
#         serializer = MessageSerializer(messages, many=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     elif request.method == "POST":
#         serializer = MessageSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# VIOLATING DRY !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# class MessageListView(APIView):
#     def get(self, request: Request) -> Response:
#         messages = Message.objects.all()
#         serializer = MessageSerializer(messages, many=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request: Request) -> Response:
#         serializer = MessageSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class TagListView(APIView):
#     def get(self, request: Request) -> Response:
#         messages = Tag.objects.all()
#         serializer = TagSerializer(messages, many=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request: Request) -> Response:
#         serializer = TagSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# USE  generics (fix SRP and DRY issues above)

# class MessageListView(generics.ListCreateAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#
#
# class TagListView(generics.ListCreateAPIView):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#


# USE viewsets for the methods-actions mapping
# ModelViewSet - implements full CRUD
class MessageViewSet(BaseViewMethodsMixin, viewsets.ModelViewSet):
    queryset = Message.objects.select_related("user").prefetch_related("tags").annotate(
        likes_count=Count("likes")
    )
    # filterset_fields = ("user",)
    filterset_class = MessageFilter
    ordering_fields = ("created_at",)
    search_fields = ["text", "user__username"]

    action_serializer_classes = {
        "list": MessageListSerializer,
        "retrieve": MessageDetailSerializer,
        "like": MessageListSerializer,
        "create": MessageSerializer,
        "update": MessageSerializer,
        "partial_update": MessageSerializer
    }

    action_permission_classes = {
        "list": [IsAuthenticated],
        "retrieve": [IsOwner],
        "delete": [IsOwner],
        "like": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsOwner],
        "partial_update": [IsOwner]
    }

    @method_decorator(cache_page(60 * 5, key_prefix="message_view"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(request=None, responses=MessageListSerializer)
    @action(detail=True, methods=["POST"], url_path="like")
    def like(self, request, pk=None):
        message = self.get_object()

        like, created = Like.objects.get_or_create(message=message, user=request.user)

        if not created:
            like.delete()

        message.likes_count = message.likes.count()
        serializer = MessageListSerializer(message)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(vary_on_headers("Authorization"))
    @method_decorator(cache_page(60 * 5, key_prefix="message_view"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# -------------------------------------OUR CUSTOM DRY FIX-------------------------------------------------------
# don't use these examples in your projects


class ListView(APIView):
    queryset = None
    serializer_class = None

    def get_queryset(self):
        assert self.queryset is not None, "define queryset attr"

        return self.queryset.all()

    def get_serializer_class(self):
        assert self.serializer_class is not None, "define serializer_class attr"

        return self.serializer_class

    def get(self, request):
        objects = self.get_queryset()
        serializer = self.get_serializer_class()(objects, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageListView(ListView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class TagListView(ListView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# --------------------------------------------Custom Generic APIView with mixins ----------------------------------
class GenericAPIView(APIView):
    queryset = None
    serializer_class = None

    def get_queryset(self):
        assert self.queryset is not None, "define queryset attr"

        return self.queryset.all()

    def get_serializer_class(self):
        assert self.serializer_class is not None, "define serializer_class attr"

        return self.serializer_class


class ListMixin:
    def list(self, request: Request) -> Response:
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateMixin:
    def create(self, request: Request) -> Response:
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCreateAPIView(ListMixin, CreateMixin, GenericAPIView):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MessageList(ListCreateAPIView):
    queryset = Message.objects.filter()
    serializer_class = MessageSerializer


class TagList(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# -------------------------------------Method - Action mapping------------------------------------------------
# get - list
# post - create
# get/<pk>/ (for detail page) - retrieve
# put (for detail page) - update
# patch (for detail page) - partial_update
# delete (for detail page) - destroy
