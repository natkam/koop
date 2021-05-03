from typing import Any, Dict, List, TYPE_CHECKING, Type, cast

from django.contrib.auth.models import AnonymousUser, User
from django.db.models import (
    OuterRef,
    QuerySet,
    Subquery,
)
from product.models import PersonalOrder, Product, ProductPersonalOrder, Week
from product.serializers import ProductPersonalOrderSerializer, ProductSerializer
from rest_framework import generics, mixins, status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

if TYPE_CHECKING:
    GenericAPIView = generics.GenericAPIView[Any]
else:
    GenericAPIView = generics.GenericAPIView


class OrderView(GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin):
    """View of the personal order of the user, allows updating the order."""

    def get(self, request: Request, week_id: int) -> Response:
        """Lists all current week products with the amounts ordered by the user."""
        return self.list(request, week_id)

    def put(self, request: Request, week_id: int) -> Response:
        """Updates the user's order, or creates a new one if it does not exist.

        Personal order update is performed by deleting all related product
        personal orders and creating new ones based on the request data.
        """
        # TODO(Nat): Only allow `put` for authenticated users.
        if isinstance(request.user, AnonymousUser):
            return Response(data="nope", status=status.HTTP_401_UNAUTHORIZED)

        personal_order, _ = PersonalOrder.objects.get_or_create(
            week_id=week_id, user=request.user
        )
        personal_order.product_personal_orders.all().delete()
        request_data = cast(List[Dict[str, Any]], request.data)
        ordered_data = [
            {
                "personal_order": personal_order.id,
                "product": data_item.get("id"),
                "amount": data_item.get("ordered_amount"),
            }
            for data_item in request_data
            if data_item.get("ordered_amount")
        ]
        serializer = self.get_serializer(data=ordered_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # TODO(Nat): Handle invalid data properly, add tests.
        return Response(status=status.HTTP_201_CREATED)

    def get_queryset(self) -> "QuerySet[Product]":
        week_id: int = self._get_week_id()
        queryset: "QuerySet[Product]" = Product.objects.filter(week=week_id)

        user = self.request.user
        if isinstance(user, AnonymousUser):
            # TODO(Nat): Fake login for now? Should it be available without login?
            return queryset

        return self._add_order_information_to_queryset(queryset, user, week_id)

    def _add_order_information_to_queryset(
        self, queryset: "QuerySet[Product]", user: User, week_id: int
    ) -> "QuerySet[Product]":
        """Annotates products with the amounts ordered by the user.

        Products that have not been ordered will have ordered_amount=None.
        """
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
        """Returns the integer id of the week, even if an alias is used in url."""
        if self.kwargs["week_id"] == "latest":
            week = Week.objects.order_by("-pickup_date").first()
            if week is not None:
                return week.id
            raise NotFound("There are no weeks to display.")

        return int(self.kwargs["week_id"])

    def get_serializer_class(self) -> "Type[BaseSerializer[Any]]":
        if self.request.method == "PUT":
            return ProductPersonalOrderSerializer
        else:
            return ProductSerializer
