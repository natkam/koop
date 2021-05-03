from product.models import PersonalOrder, Product, Week
from product.tests.factories import (
    PersonalOrderFactory,
    PersonalOrderWithOneProductFactory,
    ProductFactory,
    UserFactory,
    WeekFactory,
)
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class TestPersonalOrderEndpoint(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.week_1 = WeekFactory()
        cls.week_2 = WeekFactory()
        cls.week_3 = WeekFactory()
        cls.latest_week = Week.objects.order_by("pickup_date").last()
        cls.latest_week_url = reverse("order", kwargs={"week_id": cls.latest_week.id})
        ProductFactory.create_batch(5, week=cls.week_3)

    def test_latest_week_url_alias(self):
        response = self.client.get(reverse("order", kwargs={"week_id": "latest"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data[0].get("week"), self.latest_week.id)
        for _ in range(Product.objects.filter(week=self.latest_week).count()):
            self.assertNotIn("ordered_amount", response.data[_])

    def test_post_method_not_allowed(self):
        self.client.force_login(self.user)
        response = self.client.post(self.latest_week_url, data={"key": 42})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_method_not_allowed(self):
        self.client.force_login(self.user)
        response = self.client.delete(self.latest_week_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unauthorised_user_cannot_place_an_order(self):
        response = self.client.put(self.latest_week_url, data={"key": 42})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_sees_amounts_of_products_they_ordered(self):
        self.client.force_login(self.user)
        personal_order = PersonalOrderFactory(week=self.latest_week, user=self.user)
        product = ProductFactory(week=self.latest_week)
        amount = 1.125
        personal_order.products.add(product, through_defaults={"amount": amount})

        response = self.client.get(self.latest_week_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(amount, [product["ordered_amount"] for product in response.data])
        self.assertEqual(amount, response.data[-1]["ordered_amount"])

    def test_create_order(self):
        assert (
            PersonalOrder.objects.filter(week=self.latest_week, user=self.user).first()
            is None
        )
        self.client.force_login(self.user)
        order_data = self.client.get(self.latest_week_url).data
        order_data[0]["ordered_amount"] = 42
        order_data[2]["ordered_amount"] = 137
        ordered_products_ids = [p["id"] for p in order_data if p.get("ordered_amount")]

        response = self.client.put(self.latest_week_url, data=order_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_updated = self.client.get(self.latest_week_url)
        self.assertEqual(len(order_data), len(response_updated.data))
        self.assertListEqual(
            ordered_products_ids,
            [p["id"] for p in response_updated.data if p.get("ordered_amount")],
        )

    def test_update_existing_order(self):
        self.client.force_login(self.user)
        PersonalOrderWithOneProductFactory(week=self.latest_week, user=self.user)
        order_data = self.client.get(self.latest_week_url).data
        order_data[0]["ordered_amount"] = 42
        order_data[1]["ordered_amount"] = 0.5
        ordered_products = [p for p in order_data if p["ordered_amount"]]
        ordered_amounts = [
            p["ordered_amount"] for p in order_data if p["ordered_amount"]
        ]

        response_put = self.client.put(self.latest_week_url, data=order_data)
        self.assertEqual(response_put.status_code, status.HTTP_201_CREATED)

        response_updated = self.client.get(self.latest_week_url)
        self.assertEqual(len(order_data), len(response_updated.data))
        self.assertEqual(
            len([p for p in response_updated.data if p["ordered_amount"]]),
            len(ordered_products),
        )
        self.assertListEqual(
            [p["ordered_amount"] for p in order_data if p["ordered_amount"]],
            ordered_amounts,
        )
