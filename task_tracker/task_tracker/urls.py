from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from task_tracker.routers import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/jwt-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/jwt-token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/jwt-token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + router.urls
