from datetime import date

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


def get_current_year() -> int:
    return date.today().year


class Week(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["number", "year"], name="unique_week_number_in_year"
            ),
        ]

    number = models.PositiveIntegerField(help_text="Week number of the year")
    year = models.PositiveIntegerField(default=get_current_year)
    pickup_date = models.DateField(
        help_text="Wednesday when the orders are picked up", unique=True
    )
    coordinator = models.CharField(
        max_length=64, help_text="Name and surname of the week coordinator"
    )

    def __str__(self) -> str:
        return f"Week {self.number}/{self.year} - {self.pickup_date}"


class Pickup(models.Model):
    # TODO(Nat): Make this model more robust; add fields like role, day, ...?
    pickup = models.CharField(max_length=32)

    def __str__(self) -> str:
        return f"Pickup option: {self.pickup}"


class PersonalOrder(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "week"], name="unique_user_order_per_week"
            ),
            models.UniqueConstraint(
                fields=["week", "pickup"], name="unique_pickup_per_week"
            ),
        ]

    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    pickup = models.ForeignKey(
        Pickup,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self) -> str:
        return f"Order for {self.week.pickup_date} by {self.user.get_full_name()}"


class Product(models.Model):
    week = models.ForeignKey(Week, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=256, help_text="Name of the product, unit")
    description = models.TextField(blank=True)
    link = models.URLField(null=True, help_text="Link to the description")
    price = models.DecimalField(
        verbose_name="unit price",
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    quantity = models.PositiveIntegerField("available quantity", null=True, blank=True)

    def __str__(self) -> str:
        return self.name
