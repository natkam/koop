from django.contrib import admin

from product.models import PersonalOrder, Pickup, Product, Week


@admin.register(PersonalOrder)
class PersonalOrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Pickup)
class PickupAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    pass
