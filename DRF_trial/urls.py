from django.contrib import admin
from django.urls import path, include

from core.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('core.urls')),
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
