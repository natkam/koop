from django.test import TestCase
from product.models import Product, Week
from product.tests.factories import (
    PersonalOrderFactory,
    ProductFactory,
    ProductPersonalOrderFactory,
    UserFactory,
    WeekFactory,
)
from rest_framework.reverse import reverse


class TestPersonalOrderEndpoint(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.week_1 = WeekFactory()
        cls.week_2 = WeekFactory()
        cls.week_3 = WeekFactory()
        cls.latest_week = Week.objects.order_by("pickup_date").last()
        ProductFactory.create_batch(5, week=cls.week_3)

    def test_latest_week_url_alias(self):
        response = self.client.get(reverse("order", kwargs={"week_id": "latest"}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data[0].get("week"), self.latest_week.id)
        for _ in range(Product.objects.filter(week=self.latest_week).count()):
            self.assertNotIn("ordered_amount", response.data[_])

    def test_user_sees_ordered_amount_of_products(self):
        self.client.force_login(self.user)
        personal_order = PersonalOrderFactory(week=self.latest_week, user=self.user)
        product = ProductFactory(week=self.latest_week)
        amount = 1.125
        ProductPersonalOrderFactory(
            product=product, personal_order=personal_order, amount=amount
        )

        response = self.client.get(reverse("order", kwargs={"week_id": "latest"}))
        self.assertEqual(response.status_code, 200)
        self.assertIn(amount, [product["ordered_amount"] for product in response.data])
