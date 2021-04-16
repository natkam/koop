from typing import Any, Optional, TYPE_CHECKING

from product.models import PersonalOrder, Pickup, Product, ProductPersonalOrder, Week
from rest_framework import serializers

if TYPE_CHECKING:
    ModelSerializer = serializers.ModelSerializer[Any]
else:
    ModelSerializer = serializers.ModelSerializer


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
    ordered_amount = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_ordered_amount(self, product: Product) -> Optional[float]:
        my_product_order = product.product_personal_orders.filter(
            personal_order__user=self.context["request"].user
        ).first()
        if my_product_order:
            return my_product_order.amount
        return None


class ProductPersonalOrderSerializer(ModelSerializer):
    class Meta:
        model = ProductPersonalOrder
        fields = "__all__"
