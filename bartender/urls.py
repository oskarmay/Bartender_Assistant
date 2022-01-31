from django.urls import path

from bartender.api_views import (
    AcceptOrderApiView,
    CompleteOrderApiView,
    RejectOrderApiView,
    SetInProgressOrderApiView,
)
from bartender.views import (
    CreateCustomerAccountFormView,
    CustomerAccountDetailView,
    CustomerAccountListView,
    DrinkCreateView,
    DrinkDeleteView,
    DrinkDetailView,
    DrinkListView,
    DrinkUpdateView,
    HistoryOrdersListView,
    HomeView,
    IngredientNeededCreateView,
    IngredientNeededDeleteView,
    IngredientNeededUpdateView,
    OrdersListView,
    StorageIngredientCreateView,
    StorageIngredientDeleteView,
    StorageIngredientListView,
    StorageIngredientUpdateView,
    DrinkSuggestionsDashboardTemplateView,
    DrinkSuggestionsRandomTemplateView,
)

app_name = "bartender"
urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="home",
    ),
    path(
        "api/reject_order",
        RejectOrderApiView.as_view(),
        name="api_reject_order",
    ),
    path(
        "api/accept_order",
        AcceptOrderApiView.as_view(),
        name="api_accept_order",
    ),
    path(
        "api/in_progress_order",
        SetInProgressOrderApiView.as_view(),
        name="api_in_progress_order",
    ),
    path(
        "api/complete_order",
        CompleteOrderApiView.as_view(),
        name="api_complete_order",
    ),
    path(
        "storage_ingredient_list",
        StorageIngredientListView.as_view(),
        name="storage_ingredient_list",
    ),
    path(
        "storage_ingredient_list/create_ingredient",
        StorageIngredientCreateView.as_view(),
        name="create_ingredient",
    ),
    path(
        "storage_ingredient_list/<int:pk>/update_ingredient",
        StorageIngredientUpdateView.as_view(),
        name="update_ingredient",
    ),
    path(
        "storage_ingredient_list/<int:pk>/delete_ingredient",
        StorageIngredientDeleteView.as_view(),
        name="delete_ingredient",
    ),
    path(
        "drink_list",
        DrinkListView.as_view(),
        name="drink_list",
    ),
    path(
        "drink_list/create_drink",
        DrinkCreateView.as_view(),
        name="create_drink",
    ),
    path(
        "drink_list/<int:pk>/update_drink",
        DrinkUpdateView.as_view(),
        name="update_drink",
    ),
    path(
        "drink_list/<int:pk>/detail_drink",
        DrinkDetailView.as_view(),
        name="detail_drink",
    ),
    path(
        "drink_list/<int:pk>/delete_drink",
        DrinkDeleteView.as_view(),
        name="delete_drink",
    ),
    path(
        "ingredient_needed/create_ingredient_needed",
        IngredientNeededCreateView.as_view(),
        name="create_ingredient_needed",
    ),
    path(
        "ingredient_needed/<int:pk>/update_ingredient_needed",
        IngredientNeededUpdateView.as_view(),
        name="update_ingredient_needed",
    ),
    path(
        "ingredient_needed/<int:pk>/delete_ingredient_needed",
        IngredientNeededDeleteView.as_view(),
        name="delete_ingredient_needed",
    ),
    path(
        "orders_list",
        OrdersListView.as_view(),
        name="orders_list",
    ),
    path(
        "history_orders_list",
        HistoryOrdersListView.as_view(),
        name="history_orders_list",
    ),
    path(
        "customer/list",
        CustomerAccountListView.as_view(),
        name="customer_list",
    ),
    path(
        "customer/create_account",
        CreateCustomerAccountFormView.as_view(),
        name="create_customer_account",
    ),
    path(
        "customer/<int:pk>/user_detail",
        CustomerAccountDetailView.as_view(),
        name="customer_user_detail",
    ),
    path(
        "drink_suggestions/",
        DrinkSuggestionsDashboardTemplateView.as_view(),
        name="drink_suggestions_dashboard",
    ),
    path(
        "drink_suggestions/random",
        DrinkSuggestionsRandomTemplateView.as_view(),
        name="drink_suggestions_random",
    ),
]
