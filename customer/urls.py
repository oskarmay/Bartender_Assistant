from django.urls import path

from customer.views import HomeView, DrinkListView, SetTable

app_name = "customer"
urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="home",
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
]
