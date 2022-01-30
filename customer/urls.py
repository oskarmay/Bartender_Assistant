from django.urls import path

from customer.api_views import CancelOrderApiView, CreateOrderApiView
from customer.views import (
    HistoryOrdersListView,
    HomeView,
    MenuListView,
    OrdersListView,
    SetTable,
)

app_name = "customer"
urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="home",
    ),
    path(
        "api/create_order",
        CreateOrderApiView.as_view(),
        name="api_customer_create_order",
    ),
    path(
        "api/cancel_order",
        CancelOrderApiView.as_view(),
        name="api_customer_cancel_order",
    ),
    path(
        "set_table",
        SetTable.as_view(),
        name="set_table",
    ),
    path(
        "menu",
        MenuListView.as_view(),
        name="menu",
    ),
    path(
        "orders_list/current",
        OrdersListView.as_view(),
        name="orders_list",
    ),
    path(
        "orders_list/history",
        HistoryOrdersListView.as_view(),
        name="history_orders_list",
    ),
]
