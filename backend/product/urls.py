from rest_framework import routers

from product.views import ProductViewSet

router = routers.DefaultRouter()
router.register("", ProductViewSet)

urlpatterns = router.urls