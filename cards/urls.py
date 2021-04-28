from rest_framework.routers import DefaultRouter
from cards.views import CardsViewSet

router = DefaultRouter()
router.register(r'', CardsViewSet)

urlpatterns = router.urls
