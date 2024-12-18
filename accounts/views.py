from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Logout(APIView):
    @extend_schema(responses={status.HTTP_204_NO_CONTENT: None})
    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
