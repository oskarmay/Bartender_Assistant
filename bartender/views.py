from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)
from rules.contrib.views import PermissionRequiredMixin

from bartender.forms import (
    CreateCustomerAccountForm,
    DrinkForm,
    IngredientNeededForm,
    IngredientStorageForm,
)
from core.models import Drink, IngredientNeeded, IngredientStorage, Orders, User
from core.utilis import generate_user_with_password


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
        """Empty QS. Everything is in ctx."""

        return None

    def get_context_data(self, *, object_list=None, **kwargs):
        """Add qs over status to ctx."""

        ctx = super().get_context_data()

        ctx["orders_completed"] = (
            Orders.objects.filter(
                status=Orders.OrdersStatus.COMPLETED,
            )
            .select_related("drink", "storage_order", "user")
            .prefetch_related(
                "drink__ingredient_needed",
                "drink__ingredient_needed__storage_ingredient",
            )
            .order_by("order_date")
        )

        ctx["orders_rejected"] = (
            Orders.objects.filter(
                status=Orders.OrdersStatus.REJECTED,
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


class CreateCustomerAccountFormView(PermissionRequiredMixin, FormView):
    """View of history orders list."""

    permission_required = "is_in_staff"
    template_name = "bartender/users/create_customer_account.html"
    form_class = CreateCustomerAccountForm

    def form_valid(self, form):
        """Generating username and password and creating new customer user.
        Then redirect to user detail view with user information and login qr code."""

        additional_data = form.cleaned_data["additional_info"]
        user_data_dict = generate_user_with_password(additional_data)
        new_account = User.objects.create_user(
            username=user_data_dict["login"],
            password=user_data_dict["password"],
            one_use_account_password=user_data_dict["password"],
            expire_date=timezone.now() + timezone.timedelta(hours=13),
            role=User.Role.CUSTOMER,
        )

        self.success_url = reverse_lazy(
            "bartender:customer_user_detail", kwargs={"pk": new_account.pk}
        )

        return super().form_valid(form)


class CustomerUserDetailView(PermissionRequiredMixin, DetailView):
    """View of customer user details plus qr code to direct login."""

    permission_required = "is_in_staff"
    template_name = "bartender/users/customer_detail.html"
    model = User
    context_object_name = "user"

    def get_context_data(self, **kwargs):
        """Add to ctx link to direct user login as qr code."""

        ctx = super().get_context_data()
        host_url = self.request.META["HTTP_HOST"]
        login_url = reverse_lazy("core:login")
        query_param = f"?login={self.object.username}&password={self.object.one_use_account_password}"
        ctx["qr"] = f"{host_url}{login_url}{query_param}"

        return ctx
