from django.views.generic import TemplateView, ListView
from rules.contrib.views import PermissionRequiredMixin

from core.models import IngredientStorage


class HomeView(PermissionRequiredMixin, TemplateView):
    permission_required = "is_in_staff"
    template_name = "bartender/home.html"


class StorageListView(PermissionRequiredMixin, ListView):
    permission_required = "is_in_staff"
    template_name = "bartender/storage/list.html"
    context_object_name = "storage_ingredients"

    def get_queryset(self):
        return IngredientStorage.objects.all().order_by("type", "name")
