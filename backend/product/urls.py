from django.urls import re_path

from product.views import OrderView


urlpatterns = [
    re_path("weeks/(?P<week_id>\d+|latest)/order", OrderView.as_view(), name="order")
]
