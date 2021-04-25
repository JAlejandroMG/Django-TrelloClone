from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from boards.views import BoardViewSet

router = DefaultRouter()
router.register('Boards', BoardViewSet)


urlpatterns = [
        path('admin/', admin.site.urls)
              ] + router.urls
