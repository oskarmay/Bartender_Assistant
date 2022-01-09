from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from rules.contrib.views import PermissionRequiredMixin

from core.models import Drink, User


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
