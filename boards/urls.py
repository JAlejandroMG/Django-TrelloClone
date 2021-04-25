from rest_framework.routers import DefaultRouter

from boards.views import BoardViewSet

router = DefaultRouter()
router.register('Boards', BoardViewSet)

urlpatterns = router.urls
