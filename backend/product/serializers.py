from typing import Any, TYPE_CHECKING

from rest_framework import serializers

from product.models import Product


if TYPE_CHECKING:
    ModelSerializer = serializers.ModelSerializer[Any]
else:
    ModelSerializer = serializers.ModelSerializer


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
