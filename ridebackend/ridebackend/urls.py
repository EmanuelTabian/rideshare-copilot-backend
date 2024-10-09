from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("rideauth.urls")),
    path("api/", include("ridecalc.urls")),
    path("api/", include("rideposts.urls")),
    path("api/", include("ridecars.urls")),
    path(r"health/", include("health_check.urls")),
]
