from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

BASE_API_V1_PREFIX = 'api/v1'

urlpatterns = [
    path('admin/', admin.site.urls),

    path(f'{BASE_API_V1_PREFIX}/token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'{BASE_API_V1_PREFIX}/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path(f'{BASE_API_V1_PREFIX}/users/', include('authenticate.urls')),
    path(f'{BASE_API_V1_PREFIX}/companies/', include('company.urls')),
    path(f'{BASE_API_V1_PREFIX}/storages/', include('storage.urls')),

    path(f'{BASE_API_V1_PREFIX}/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(f'{BASE_API_V1_PREFIX}/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger_ui')
]