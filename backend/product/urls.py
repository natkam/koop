from rest_framework import routers

from product.views import ProductViewSet

router = routers.DefaultRouter()
router.register(
    "weeks/(?P<week_id>\d+|latest)/order", ProductViewSet, basename="product"
)

urlpatterns = router.urls
