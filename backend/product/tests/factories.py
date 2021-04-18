import datetime as dt

import factory
from django.contrib.auth.models import User
from factory import fuzzy
from factory.django import DjangoModelFactory
from product.models import PersonalOrder, Pickup, Product, ProductPersonalOrder, Week


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.LazyAttribute(lambda o: f"{o.first_name}_{o.last_name}")
    password = "pass"


class WeekFactory(DjangoModelFactory):
    class Meta:
        model = Week

    number = factory.Sequence(lambda n: n + 1)
    year = 2021
    pickup_date = factory.Sequence(lambda n: dt.date(2021, 1, 1) + dt.timedelta(days=n))
    coordinator = factory.Faker("name")


class PickupFactory(DjangoModelFactory):
    class Meta:
        model = Pickup

    description = factory.Faker("text", max_nb_chars=20)


class PersonalOrderFactory(DjangoModelFactory):
    week = factory.SubFactory(WeekFactory)
    user = factory.SubFactory(UserFactory)
    pickup = factory.SubFactory(PickupFactory)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    week = factory.SubFactory(WeekFactory)
    name = factory.Faker("text", max_nb_chars=64)
    description = factory.Faker("text", max_nb_chars=128)
    link = factory.Faker("uri")
    price = fuzzy.FuzzyDecimal(30)
    quantity = fuzzy.FuzzyInteger(1, 100)


class ProductPersonalOrderFactory(DjangoModelFactory):
    class Meta:
        model = ProductPersonalOrder

    personal_order = factory.SubFactory(PersonalOrderFactory)
    product = factory.SubFactory(ProductFactory)
    amount = fuzzy.FuzzyFloat(0.1, 5)


class PersonalOrderWithOneProductFactory(PersonalOrderFactory):
    class Meta:
        model = PersonalOrder

    product = factory.RelatedFactory(
        ProductPersonalOrderFactory, factory_related_name="personal_order"
    )


class PersonalOrderWithTwoProductsFactory(PersonalOrderFactory):
    product_1 = factory.RelatedFactory(
        ProductPersonalOrderFactory,
        factory_related_name="personal_order",
        product__name="Oliwki Kalamata",
    )
    product_2 = factory.RelatedFactory(
        ProductPersonalOrderFactory,
        factory_related_name="personal_order",
        product__name="Chleb orkiszowy",
    )
