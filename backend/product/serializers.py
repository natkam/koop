from typing import Any, Dict, List, TYPE_CHECKING

from django.db.models import QuerySet
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


class ProductPersonalOrderListSerializer(ListSerializer):
    def update(
        self,
        instance: "QuerySet[ProductPersonalOrder]",
        validated_data: List[Dict[str, Any]],
    ) -> List[ProductPersonalOrder]:
        """Updates ordered products in a personal order.

        When a product is added to a personal order, a new ProductPersonalOrder
        (M2M relation) is created. When amount of an ordered product is changed, the
        existing ProductPersonalOrder object is updated. When amount of an ordered
        product is set to a falsey value (`null` or 0), the ProductPersonalOrder
        relation is deleted from the database.

        The implementation is based on the example in the docs:
        https://www.django-rest-framework.org/api-guide/serializers/#customizing-multiple-update

        Args:
            instance: Queryset of ProductPersonalOrders, i.e. the products ordered by
                the user this week (before the update).
            validated_data: List of dicts representing the ProductPersonalOrders after
                the update; PPOs where the ordered amount is not null nor 0.

        Returns:
            List of ProductPersonalOrders representing the products ordered by the user.
        """
        # Perform creations and updates.
        ordered = []
        ordered_ids = []
        for ppo_data in validated_data:
            ppo, created = instance.update_or_create(
                personal_order=ppo_data["personal_order"],
                product=ppo_data["product"],
                defaults=ppo_data,
            )
            ordered.append(ppo)
            ordered_ids.append(ppo.id)
        # TODO(Nat): Make sure only the ordered amount data can be altered by the user.

        # Perform deletions.
        for ppo in instance:
            if ppo.id not in ordered_ids:
                ppo.delete()

        return ordered


class ProductPersonalOrderSerializer(ModelSerializer):
    class Meta:
        model = ProductPersonalOrder
        list_serializer_class = ProductPersonalOrderListSerializer
        fields = "__all__"
