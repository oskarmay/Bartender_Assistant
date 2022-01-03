from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from rules.contrib.views import PermissionRequiredMixin

from core.models import IngredientStorage

from bartender.forms import IngredientForm


class HomeView(PermissionRequiredMixin, TemplateView):
    permission_required = "is_in_staff"
    template_name = "bartender/home.html"


class StorageListView(PermissionRequiredMixin, ListView):
    permission_required = "is_in_staff"
    template_name = "bartender/storage/list_ingredient.html"
    context_object_name = "storage_ingredients"

    def get_queryset(self):
        return IngredientStorage.objects.all().order_by("type", "name")


class IngredientCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "is_in_staff"
    template_name = "bartender/storage/create_ingredient.html"
    model = IngredientStorage
    success_url = reverse_lazy("bartender:storage_list")
    form_class = IngredientForm


class IngredientUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "is_in_staff"
    template_name = "bartender/storage/update_ingredient.html"
    model = IngredientStorage
    success_url = reverse_lazy("bartender:storage_list")
    form_class = IngredientForm


class IngredientDeleteView(PermissionRequiredMixin, DeleteView):
    model = IngredientStorage
    context_object_name = "storage_ingredient"
    permission_required = "is_in_staff"
    template_name = "bartender/storage/delete_ingredient.html"
    success_url = reverse_lazy("bartender:storage_list")
