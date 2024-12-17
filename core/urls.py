from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from rest_framework.authtoken import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),

    # apps
    path("api/", include("messenger.urls")),
    path("api/accounts/", include("accounts.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
