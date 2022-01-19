from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from rules.contrib.views import PermissionRequiredMixin

from core.models import Drink, IngredientStorage, Orders, User


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


class MenuListView(PermissionRequiredMixin, ListView):
    """View of orders list."""

    permission_required = "customer"
    template_name = "customer/orders/list_order.html"
    context_object_name = "drinks"

    def get_queryset(self):
        """Prefetch related field of orders object (reduced sql)."""

        return (
            Drink.objects.all()
            .order_by("type", "name")
            .prefetch_related(
                "ingredient_needed", "ingredient_needed__storage_ingredient"
            )
            .order_by("name")
            .filter(is_possible_to_make=True)
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        """Add to context other ingredient that can be ordered."""

        ctx = super().get_context_data()
        ctx["other_orders"] = IngredientStorage.objects.filter(
            can_be_ordered=True
        ).order_by("type")
        return ctx


class OrdersListView(PermissionRequiredMixin, ListView):
    """View of orders list."""

    permission_required = "customer"
    template_name = "customer/orders/list_ordered.html"
    context_object_name = "orders"

    def get_queryset(self):
        """Getting only ordered orders with status created, accepted and in progress.
        Prefetch related field of drinkqueue object (reduced sql)."""

        user = self.request.user
        return (
            Orders.objects.filter(
                user=user,
                status__in=[
                    Orders.OrdersStatus.CREATED,
                    Orders.OrdersStatus.ACCEPTED,
                    Orders.OrdersStatus.IN_PROGRESS,
                ],
            )
            .select_related("drink", "storage_order")
            .prefetch_related(
                "drink__ingredient_needed",
                "drink__ingredient_needed__storage_ingredient",
            )
            .order_by("-order_date")
        )


class HistoryOrdersListView(PermissionRequiredMixin, ListView):
    """View of history orderes list."""

    permission_required = "customer"
    template_name = "customer/orders/history_list_ordered.html"  #
    context_object_name = "orders"

    def get_queryset(self):
        """Getting only ordered orders with status created, accepted and in progress.
        Prefetch related field of drinkqueue object (reduced sql)."""

        user = self.request.user
        return (
            Orders.objects.filter(
                user=user,
                status__in=[
                    Orders.OrdersStatus.REJECTED,
                    Orders.OrdersStatus.COMPLETED,
                    Orders.OrdersStatus.CANCELED,
                ],
            )
            .select_related("drink", "storage_order")
            .prefetch_related(
                "drink__ingredient_needed",
                "drink__ingredient_needed__storage_ingredient",
            )
            .order_by("-order_date")
        )
