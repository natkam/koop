from typing import Any, TYPE_CHECKING

from product.models import PersonalOrder, Pickup, Product, ProductPersonalOrder, Week
from rest_framework import serializers

if TYPE_CHECKING:
    ModelSerializer = serializers.ModelSerializer[Any]
    ListSerializer = serializers.ListSerializer[Any]
else:
    ModelSerializer = serializers.ModelSerializer
    ListSerializer = serializers.ListSerializer


class WeekSerializer(ModelSerializer):
    class Meta:
        model = Week
        fields = "__all__"


class PickupSerializer(ModelSerializer):
    class Meta:
        model = Pickup
        fields = "__all__"


class PersonalOrderSerializer(ModelSerializer):
    class Meta:
        model = PersonalOrder
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    ordered_amount = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "link",
            "price",
            "quantity",
            "week",
            "ordered_amount",
        ]


class ProductPersonalOrderSerializer(ModelSerializer):
    class Meta:
        model = ProductPersonalOrder
        fields = ["id", "product", "personal_order", "amount"]
