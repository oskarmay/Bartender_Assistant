from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from rules.contrib.views import PermissionRequiredMixin

from core.models import Drink, DrinkQueue, User


class HomeView(PermissionRequiredMixin, TemplateView):
    """View of customer homepage."""

    permission_required = "customer"
    template_name = "customer/home.html"


class SetTable(PermissionRequiredMixin, TemplateView):
    """View of setting up customer table."""

    permission_required = "customer"
    template_name = "customer/set_table.html"

    def post(self, request):
        if "save_table" in self.request.POST:
            table = self.request.POST.get("table")
            user = User.objects.get(pk=self.request.user.id)
            user.customer_table = table
            user.save()
        return redirect(reverse_lazy("customer:home"))


class DrinkListView(PermissionRequiredMixin, ListView):
    """View of drink list."""

    permission_required = "customer"
    template_name = "customer/drink/list_drink.html"
    context_object_name = "drinks"

    def get_queryset(self):
        """Prefetch related field of drink object (reduced sql)."""
        return (
            Drink.objects.all()
            .order_by("type", "name")
            .prefetch_related(
                "ingredient_needed", "ingredient_needed__storage_ingredient"
            )
            # .filter(is_possible_to_make=True)  # TODO uncomment after creating small db
        )


class OrdersListView(PermissionRequiredMixin, ListView):
    """View of orders list."""

    permission_required = "customer"
    template_name = "customer/drink/list_drink_ordered.html"
    context_object_name = "drinks"

    def get_queryset(self):
        """Getting only ordered drink with status created, accepted and in progress.
        Prefetch related field of drinkqueue object (reduced sql)."""

        user = self.request.user
        return (
            DrinkQueue.objects.filter(
                user=user,
                status__in=[
                    DrinkQueue.DrinkQueueStatus.CREATED,
                    DrinkQueue.DrinkQueueStatus.ACCEPTED,
                    DrinkQueue.DrinkQueueStatus.IN_PROGRESS,
                ],
            )
            .select_related("drink")
            .prefetch_related(
                "drink__ingredient_needed",
                "drink__ingredient_needed__storage_ingredient",
            )
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        """TODO"""

        ctx = super().get_context_data()
        ctx[
            "other_orders"
        ] = ""  # TODO Utworzyć model do zamawiania przekasek i tutaj wstawic qs do tego;

        return ctx


class HistoryOrdersListView(PermissionRequiredMixin, ListView):
    """View of history orderes list."""

    permission_required = "customer"
    template_name = "customer/drink/history_list_drink_ordered.html"
    context_object_name = "drinks"

    def get_queryset(self):
        """Getting only ordered drink with status created, accepted and in progress.
        Prefetch related field of drinkqueue object (reduced sql)."""

        user = self.request.user
        return (
            DrinkQueue.objects.filter(
                user=user,
                status__in=[
                    DrinkQueue.DrinkQueueStatus.REJECTED,
                    DrinkQueue.DrinkQueueStatus.COMPLETED,
                    DrinkQueue.DrinkQueueStatus.CANCELED,
                ],
            )
            .select_related("drink")
            .prefetch_related(
                "drink__ingredient_needed",
                "drink__ingredient_needed__storage_ingredient",
            )
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        """TODO"""

        ctx = super().get_context_data()
        ctx[
            "other_orders"
        ] = ""  # TODO Utworzyć model do zamawiania przekasek i tutaj wstawic qs do tego;

        return ctx
