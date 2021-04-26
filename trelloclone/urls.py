from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('lists/', include('lists.urls')),
    path('boards/', include('boards.urls')),
    path('comments/', include('comments.urls')),
    path('cards/', include('cards.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]