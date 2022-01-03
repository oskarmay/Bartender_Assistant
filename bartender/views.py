from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from rules.contrib.views import PermissionRequiredMixin

from core.models import IngredientStorage, Drink

from bartender.forms import IngredientStorageForm, DrinkForm


class HomeView(PermissionRequiredMixin, TemplateView):
    permission_required = "is_in_staff"
    template_name = "bartender/home.html"


class StorageIngredientListView(PermissionRequiredMixin, ListView):
    permission_required = "is_in_staff"
    template_name = "bartender/storage/list_ingredient.html"
    context_object_name = "storage_ingredients"

    def get_queryset(self):
        return IngredientStorage.objects.all().order_by("type", "name")


class StorageIngredientCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "is_in_staff"
    template_name = "bartender/storage/create_ingredient.html"
    model = IngredientStorage
    success_url = reverse_lazy("bartender:storage_ingredient_list")
    form_class = IngredientStorageForm


class StorageIngredientUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "is_in_staff"
    template_name = "bartender/storage/update_ingredient.html"
    model = IngredientStorage
    success_url = reverse_lazy("bartender:storage_ingredient_list")
    form_class = IngredientStorageForm


class StorageIngredientDeleteView(PermissionRequiredMixin, DeleteView):
    model = IngredientStorage
    context_object_name = "storage_ingredient"
    permission_required = "is_in_staff"
    template_name = "bartender/storage/delete_ingredient.html"
    success_url = reverse_lazy("bartender:drink_list")


class DrinkListView(PermissionRequiredMixin, ListView):
    permission_required = "is_in_staff"
    template_name = "bartender/drink/list_drink.html"
    context_object_name = "drinks"

    def get_queryset(self):
        return Drink.objects.all().order_by("type", "name")


class DrinkCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "is_in_staff"
    template_name = "bartender/drink/create_drink.html"
    model = Drink
    success_url = reverse_lazy("bartender:drink_list")
    form_class = DrinkForm


class DrinkDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "is_in_staff"
    template_name = "bartender/drink/detail_drink.html"
    model = Drink
    context_object_name = "drink"


class DrinkUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "is_in_staff"
    template_name = "bartender/drink/update_drink.html"
    model = Drink
    form_class = DrinkForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("bartender:detail_drink", args=(self.object.id,))


class DrinkDeleteView(PermissionRequiredMixin, DeleteView):
    model = Drink
    context_object_name = "drink"
    permission_required = "is_in_staff"
    template_name = "bartender/drink/delete_drink.html"
    success_url = reverse_lazy("bartender:drink_list")
