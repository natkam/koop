from typing import Any, TYPE_CHECKING

from django.contrib.auth.models import AnonymousUser
from django.db.models import (
    OuterRef,
    QuerySet,
    Subquery,
)
from product.models import PersonalOrder, Product, ProductPersonalOrder, Week
from product.serializers import ProductPersonalOrderSerializer, ProductSerializer
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response

if TYPE_CHECKING:
    GenericAPIView = generics.GenericAPIView[Any]
else:
    GenericAPIView = generics.GenericAPIView


class OrderView(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request: Request, week_id: int) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def put(self, request: Request, week_id: int) -> Response:
        # TODO(Nat): 1. Split this View in two: one for `get`, another for `put`.
        # TODO(Nat): 2. Only allow `put` for authenticated users.
        if isinstance(request.user, AnonymousUser):
            return Response(data="nope", status=status.HTTP_401_UNAUTHORIZED)

        personal_order = PersonalOrder.objects.filter(
            week=week_id, user=request.user
        ).first()
        if personal_order is None:
            # TODO(Nat): Create a personal order + product-personal-orders.
            return Response(data="No personal order yet. We're working on it.")

        queryset = personal_order.product_personal_orders.all()
        ordered_data = [
            {
                "personal_order": personal_order.id,
                "product": data_item["id"],
                "amount": data_item["ordered_amount"],
            }
            for data_item in request.data
            if data_item["ordered_amount"] is not None
        ]
        serializer = ProductPersonalOrderSerializer(
            queryset, data=ordered_data, many=True
        )
        if serializer.is_valid(raise_exception=True):
            for ppo_data in serializer.validated_data:
                ppo, created = queryset.update_or_create(
                    personal_order=ppo_data["personal_order"],
                    product=ppo_data["product"],
                    defaults=ppo_data,
                )
            return self.get(request, week_id=week_id)
            # TODO(Nat): Implement `update` in a ListSerializer of ProductPersonalOrders.
            # TODO(Nat): Handle deleting products from a personal order!

        return Response("Wrong data. What a pity!", status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self) -> "QuerySet[Product]":
        week_id: int = self._get_week_id()
        queryset: "QuerySet[Product]" = Product.objects.filter(week=week_id)

        user = self.request.user
        if isinstance(user, AnonymousUser):
            # TODO(Nat): Fake logging in for now; get_or_create a user.
            return queryset

        user_orders = PersonalOrder.objects.filter(user=user, week=week_id)
        if user_orders.first() is not None:
            user_product_order = ProductPersonalOrder.objects.filter(
                personal_order__user=user,
                personal_order__week_id=week_id,
                product=OuterRef("pk"),
            )[:1]
            queryset = queryset.annotate(
                ordered_amount=Subquery(user_product_order.values("amount")[:1])
            )

        return queryset

    def _get_week_id(self) -> int:
        if self.kwargs["week_id"] == "latest":
            week = Week.objects.order_by("-pickup_date").first()
            if week is not None:
                return week.id
            raise NotFound("There are no weeks to display.")

        return int(self.kwargs["week_id"])
