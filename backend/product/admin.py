import typing

from django.contrib import admin

from product.models import PersonalOrder, Pickup, Product, Week


if typing.TYPE_CHECKING:
    ModelAdmin = admin.ModelAdmin[typing.Any]
else:
    ModelAdmin = admin.ModelAdmin


@admin.register(PersonalOrder)
class PersonalOrderAdmin(ModelAdmin):
    pass


@admin.register(Pickup)
class PickupAdmin(ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    pass


@admin.register(Week)
class WeekAdmin(ModelAdmin):
    pass
