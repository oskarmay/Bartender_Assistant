from django.urls import path

from customer.views import HomeView

app_name = "customer"
urlpatterns = [
    path(
        "",
        HomeView.as_view(),
        name="home",
    ),
]
