from django.db import IntegrityError
from django.test import TestCase
from product.models import PersonalOrder, ProductPersonalOrder
from product.tests.factories import (
    PersonalOrderWithOneProductFactory,
    PickupFactory,
    UserFactory,
    WeekFactory,
)


class TestPersonalOrderModel(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = UserFactory()
        cls.user_2 = UserFactory()
        cls.week = WeekFactory()
        cls.pickup_1 = PickupFactory()
        cls.pickup_2 = PickupFactory()

    def test_one_user_can_have_one_order_per_week(self):
        PersonalOrder.objects.create(
            user=self.user_1, week=self.week, pickup=self.pickup_1
        )
        with self.assertRaises(IntegrityError):
            PersonalOrder.objects.create(
                user=self.user_1, week=self.week, pickup=self.pickup_2
            )

    def test_two_orders_cannot_have_the_same_pickup(self):
        PersonalOrder.objects.create(
            user=self.user_1, week=self.week, pickup=self.pickup_1
        )
        with self.assertRaises(IntegrityError):
            PersonalOrder.objects.create(
                user=self.user_2, week=self.week, pickup=self.pickup_1
            )

    def test_product_can_only_be_added_once_to_personal_order(self):
        personal_order = PersonalOrderWithOneProductFactory(week=self.week)
        product = personal_order.products.first()
        with self.assertRaises(IntegrityError):
            ProductPersonalOrder.objects.create(
                product=product, personal_order=personal_order, amount=1
            )
