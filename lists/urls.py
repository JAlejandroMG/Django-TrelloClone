from rest_framework.routers import DefaultRouter

from lists.views import ListViewSet

router = DefaultRouter()
router.register('', ListViewSet)

urlpatterns = router.urls
