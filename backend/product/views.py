from typing import Any

from django.contrib.auth.models import AnonymousUser
from django.db.models import (
    Model,
    OuterRef,
    QuerySet,
    Subquery,
)
from django.http import Http404
from product.models import PersonalOrder, Product, ProductPersonalOrder, Week
from product.serializers import ProductSerializer
from rest_framework import viewsets


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self) -> "QuerySet[Model]":
        week_id: int = self._get_week_id()
        queryset: "QuerySet[Any]" = Product.objects.filter(week=week_id)

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
            raise Http404("There are no weeks to display.")

        return int(self.kwargs["week_id"])
