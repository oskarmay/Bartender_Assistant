from django.urls import path

from bartender.views import (
    HomeView,
    StorageIngredientListView,
    StorageIngredientCreateView,
    StorageIngredientUpdateView,
    StorageIngredientDeleteView,
    DrinkListView,
    DrinkCreateView,
    DrinkUpdateView,
    DrinkDeleteView,
    DrinkDetailView,
)

app_name = "bartender"
urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="home",
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
]
