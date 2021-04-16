from typing import Any

from django.contrib.auth.models import AnonymousUser
from django.db.models import Model, QuerySet, Value
from django.http import Http404
from product.models import PersonalOrder, Product, Week
from product.serializers import ProductSerializer
from rest_framework import viewsets


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self) -> "QuerySet[Model]":
        week_id: int = self._get_week_id()
        user = self.request.user
        if not isinstance(user, AnonymousUser):
            user_product_order = PersonalOrder.objects.filter(
                user=user.id, week=week_id
            ).first()
        queryset: "QuerySet[Any]" = Product.objects.filter(week=week_id)
        if user_product_order:
            queryset = (
                queryset.select_related("week")
                .prefetch_related("product_personal_orders__personal_order__user")
                .annotate(ordered_amount=Value(42))
            )

        return queryset

    def _get_week_id(self) -> int:
        if self.kwargs["week_id"] == "latest":
            week = Week.objects.order_by("-pickup_date").first()
            if week is not None:
                return week.id
            raise Http404("There are no weeks to display.")

        return int(self.kwargs["week_id"])
