from django.views.generic import TemplateView
from rules.contrib.views import PermissionRequiredMixin


class HomeView(PermissionRequiredMixin, TemplateView):
    permission_required = "is_in_staff"
    template_name = "bartender/home.html"
