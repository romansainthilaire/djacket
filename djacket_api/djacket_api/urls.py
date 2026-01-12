from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import TokenRefreshView

from users.views import CustomTokenObtainPairView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/", include("users.urls")),
    path("api/v1/", include("products.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
