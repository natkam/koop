from rest_framework import viewsets

from product.models import Product
from product.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("week")
    serializer_class = ProductSerializer
