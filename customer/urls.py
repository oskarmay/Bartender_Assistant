from django.urls import path

from customer.api_views import CancelOrderedDrinkApiView, OrderDrinkApiView
from customer.views import DrinkListView, HomeView, OrdersListView, SetTable

app_name = "customer"
urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="home",
    ),
    path(
        "api/order_drink",
        OrderDrinkApiView.as_view(),
        name="api_customer_order_drink",
    ),
    path(
        "api/cancel_order_drink",
        CancelOrderedDrinkApiView.as_view(),
        name="api_customer_cancel_ordered_drink",
    ),
    path(
        "set_table",
        SetTable.as_view(),
        name="set_table",
    ),
    path(
        "drink_list",
        DrinkListView.as_view(),
        name="drink_list",
    ),
    path(
        "orders_list",
        OrdersListView.as_view(),
        name="orders_list",
    ),
]
