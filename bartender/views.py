from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from rules.contrib.views import PermissionRequiredMixin

from bartender.forms import DrinkForm, IngredientNeededForm, IngredientStorageForm
from core.models import Drink, IngredientNeeded, IngredientStorage, Orders


class HomeView(PermissionRequiredMixin, TemplateView):
    """View of bartender homepage."""

    permission_required = "is_in_staff"
    template_name = "bartender/home.html"


class StorageIngredientListView(PermissionRequiredMixin, ListView):
    """View of ingredients in storage list."""

    permission_required = "is_in_staff"
    template_name = "bartender/storage/list_ingredient.html"
    context_object_name = "storage_ingredients"

    def get_queryset(self):
        """Return storage ingredient ordered by type and name."""
        return IngredientStorage.objects.all().order_by("type", "name")


class StorageIngredientCreateView(PermissionRequiredMixin, CreateView):
    """View of adding new ingredient to storage."""

    permission_required = "is_in_staff"
    template_name = "bartender/storage/create_ingredient.html"
    model = IngredientStorage
    form_class = IngredientStorageForm
    success_url = reverse_lazy("bartender:storage_ingredient_list")


class StorageIngredientUpdateView(PermissionRequiredMixin, UpdateView):
    """View of editing ingredient from storage"""

    permission_required = "is_in_staff"
    template_name = "bartender/storage/update_ingredient.html"
    model = IngredientStorage
    form_class = IngredientStorageForm
    success_url = reverse_lazy("bartender:storage_ingredient_list")


class StorageIngredientDeleteView(PermissionRequiredMixin, DeleteView):
    """View of deleting ingredient from storage. This also delete related ingredient needed for drink."""

    permission_required = "is_in_staff"
    template_name = "bartender/storage/delete_ingredient.html"
    model = IngredientStorage
    context_object_name = "storage_ingredient"
    success_url = reverse_lazy("bartender:storage_ingredient_list")


class DrinkListView(PermissionRequiredMixin, ListView):
    """View of drink list."""

    permission_required = "is_in_staff"
    template_name = "bartender/drink/list_drink.html"
    context_object_name = "drinks"

    def get_queryset(self):
        """Prefetch related field of drink object (reduced sql)."""
        return (
            Drink.objects.all()
            .order_by("type", "name")
            .prefetch_related(
                "ingredient_needed", "ingredient_needed__storage_ingredient"
            )
        )


class DrinkCreateView(PermissionRequiredMixin, CreateView):
    """View of adding new drink."""

    permission_required = "is_in_staff"
    template_name = "bartender/drink/create_drink.html"
    model = Drink
    form_class = DrinkForm

    def get_success_url(self, **kwargs):
        """When success redirect to create ingredient_needed with drink id in query param."""
        return (
            reverse_lazy("bartender:create_ingredient_needed")
            + f"?drink={self.object.id}"
        )


class DrinkUpdateView(PermissionRequiredMixin, UpdateView):
    """View of editing drink."""

    permission_required = "is_in_staff"
    template_name = "bartender/drink/update_drink.html"
    model = Drink
    form_class = DrinkForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("bartender:detail_drink", args=(self.object.id,))


class DrinkDetailView(PermissionRequiredMixin, DetailView):
    """View of drink detail"""

    permission_required = "is_in_staff"
    template_name = "bartender/drink/detail_drink.html"
    model = Drink
    context_object_name = "drink"

    def get_context_data(self, **kwargs):
        """Add ingredient needed to drink prepare to context"""
        ctx = super().get_context_data(**kwargs)
        ctx["ingredient_needed"] = IngredientNeeded.objects.filter(
            drink_id=self.object.id
        ).select_related("storage_ingredient")
        return ctx


class DrinkDeleteView(PermissionRequiredMixin, DeleteView):
    """View of deleting drink."""

    permission_required = "is_in_staff"
    template_name = "bartender/drink/delete_drink.html"
    model = Drink
    context_object_name = "drink"
    success_url = reverse_lazy("bartender:drink_list")


class IngredientNeededCreateView(PermissionRequiredMixin, CreateView):
    """View of ingredient needed for drink preparation."""

    permission_required = "is_in_staff"
    template_name = "bartender/ingredient_needed/create_ingredient_needed.html"
    model = IngredientNeeded
    form_class = IngredientNeededForm

    def get_context_data(self, **kwargs):
        """Add related drink object to ctx."""
        ctx = super().get_context_data(**kwargs)
        ctx["drink"] = Drink.objects.filter(pk=self.request.GET.get("drink")).first()
        return ctx

    def get_success_url(self, **kwargs):
        return reverse_lazy("bartender:detail_drink", args=(self.object.drink.id,))


class IngredientNeededUpdateView(PermissionRequiredMixin, UpdateView):
    """View of editing ingredient needed."""

    permission_required = "is_in_staff"
    template_name = "bartender/ingredient_needed/update_ingredient_needed.html"
    model = IngredientNeeded
    form_class = IngredientNeededForm

    def get_context_data(self, **kwargs):
        """Add related drink object to ctx."""

        ctx = super().get_context_data(**kwargs)
        ctx["drink"] = Drink.objects.filter(ingredient_needed=self.object.pk).first()
        return ctx

    def get_success_url(self, **kwargs):
        return reverse_lazy("bartender:detail_drink", args=(self.object.drink.id,))


class IngredientNeededDeleteView(PermissionRequiredMixin, DeleteView):
    """View of delete ingredient needed."""

    permission_required = "is_in_staff"
    template_name = "bartender/ingredient_needed/delete_ingredient_needed.html"
    model = IngredientNeeded
    context_object_name = "ingredient_needed"

    def get_success_url(self):
        return reverse_lazy("bartender:detail_drink", args=(self.object.drink.id,))


class OrdersListView(PermissionRequiredMixin, ListView):
    """View of orders list."""

    permission_required = "is_in_staff"
    template_name = "bartender/orders/list_queue.html"
    context_object_name = "drinks"

    def get_queryset(self):
        """Empty QS. Everything is in ctx."""

        return None

    def get_context_data(self, *, object_list=None, **kwargs):
        """Add qs over status to ctx."""

        ctx = super().get_context_data()

        ctx["orders_created"] = (
            Orders.objects.filter(
                status=Orders.OrdersStatus.CREATED,
            )
            .select_related("drink", "storage_order", "user")
            .prefetch_related(
                "drink__ingredient_needed",
                "drink__ingredient_needed__storage_ingredient",
            )
            .order_by("order_date")
        )

        ctx["orders_accepted"] = (
            Orders.objects.filter(
                status=Orders.OrdersStatus.ACCEPTED,
            )
            .select_related("drink", "storage_order", "user")
            .prefetch_related(
                "drink__ingredient_needed",
                "drink__ingredient_needed__storage_ingredient",
            )
            .order_by("order_date")
        )
        ctx["orders_in_progress"] = (
            Orders.objects.filter(
                status=Orders.OrdersStatus.IN_PROGRESS,
            )
            .select_related("drink", "storage_order", "user")
            .prefetch_related(
                "drink__ingredient_needed",
                "drink__ingredient_needed__storage_ingredient",
            )
            .order_by("order_date")
        )

        return ctx


class HistoryOrdersListView(PermissionRequiredMixin, ListView):
    """View of history orders list."""

    permission_required = "is_in_staff"
    template_name = "bartender/orders/list_history_queue.html"
    context_object_name = "drinks"

    def get_queryset(self):
        """Qs with currently pending orders orders."""

        return (
            Orders.objects.filter(
                status__in=[
                    Orders.OrdersStatus.CANCELED,
                    Orders.OrdersStatus.REJECTED,
                    Orders.OrdersStatus.COMPLETED,
                ],
                drink__isnull=False,
                storage_order__isnull=True,
            )
            .select_related("drink")
            .prefetch_related(
                "drink__ingredient_needed",
                "drink__ingredient_needed__storage_ingredient",
            )
            .order_by("-order_date")
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        """Add qs of order other than orders to ctx."""

        ctx = super().get_context_data()
        ctx["other_orders"] = (
            Orders.objects.filter(
                status__in=[
                    Orders.OrdersStatus.CANCELED,
                    Orders.OrdersStatus.REJECTED,
                    Orders.OrdersStatus.COMPLETED,
                ],
                drink__isnull=True,
                storage_order__isnull=False,
            )
            .select_related("storage_order")
            .order_by("-order_date")
        )

        return ctx
