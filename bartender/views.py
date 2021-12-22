from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView
from rules.contrib.views import PermissionRequiredMixin

from core.models import IngredientStorage

from bartender.forms import IngredientCreateForm


class HomeView(PermissionRequiredMixin, TemplateView):
    permission_required = "is_in_staff"
    template_name = "bartender/home.html"


class StorageListView(PermissionRequiredMixin, ListView):
    permission_required = "is_in_staff"
    template_name = "bartender/storage/list.html"
    context_object_name = "storage_ingredients"

    def get_queryset(self):
        return IngredientStorage.objects.all().order_by("type", "name")


class IngredientCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "is_in_staff"
    template_name = "bartender/storage/add_ingredient.html"
    model = IngredientStorage
    success_url = reverse_lazy("bartender:storage_list")
    form_class = IngredientCreateForm
