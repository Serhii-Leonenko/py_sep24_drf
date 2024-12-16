from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from accounts.views import Logout, UserViewSet

app_name = "accounts"

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),

    # obtain token
    path("api-token-auth/", obtain_auth_token),
    path("logout/", Logout.as_view()),
]
