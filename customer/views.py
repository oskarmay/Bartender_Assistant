from django.views.generic import TemplateView
from rules.contrib.views import PermissionRequiredMixin


class HomeView(PermissionRequiredMixin, TemplateView):
    permission_required = "customer"
    template_name = "customer/home.html"
