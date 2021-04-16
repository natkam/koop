from typing import Any, Optional, TYPE_CHECKING

from django.contrib import admin
from django.db.models import ForeignKey
from django.forms import ModelChoiceField
from django.http import HttpRequest
from product.models import PersonalOrder, Pickup, Product, ProductPersonalOrder, Week

if TYPE_CHECKING:
    ModelAdmin = admin.ModelAdmin[Any]
    TabularInline = admin.TabularInline[Any]
else:
    ModelAdmin = admin.ModelAdmin
    TabularInline = admin.TabularInline


class ProductPersonalOrderInline(TabularInline):
    model = ProductPersonalOrder

    def formfield_for_foreignkey(
        self,
        db_field: "ForeignKey[Any, Any]",
        request: Optional[HttpRequest],
        **kwargs: Any,
    ) -> Optional[ModelChoiceField]:
        """Limit products to the current week."""
        if db_field.name == "product" and request is not None:
            personal_order_id = request.resolver_match.kwargs.get("object_id")
            if personal_order_id is not None:
                week = PersonalOrder.objects.get(pk=personal_order_id).week
                kwargs["queryset"] = Product.objects.filter(week=week).distinct()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(PersonalOrder)
class PersonalOrderAdmin(ModelAdmin):
    inlines = [ProductPersonalOrderInline]
    list_display = ["__str__", "pickup"]
    list_filter = ["week", "user"]


@admin.register(Pickup)
class PickupAdmin(ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ["__str__", "week"]
    list_filter = ["week"]


@admin.register(Week)
class WeekAdmin(ModelAdmin):
    list_display = ["__str__", "coordinator"]
