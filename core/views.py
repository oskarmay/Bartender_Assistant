from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import TemplateView

from core.forms import CustomChangePasswordForm


class HomeView(TemplateView):
    template_name = "core/home.html"


def error_404(request, exception):
    if request.user.is_customer:
        base = "customer/base.html"
    elif request.user.is_bartender:
        base = "bartender/base.html"
    else:
        base = "core/base.html"

    context = {"base_template": base}
    return render(request, "core/404.html", context)


def error_403(request, exception):
    if request.user.is_customer:
        base = "customer/base.html"
    elif request.user.is_bartender:
        base = "bartender/base.html"
    else:
        base = "core/base.html"

    context = {"base_template": base}
    return render(request, "core/404.html", context)


def error_500(request):
    if request.user.is_customer:
        base = "customer/base.html"
    elif request.user.is_bartender:
        base = "bartender/base.html"
    else:
        base = "core/base.html"

    context = {"base_template": base}
    return render(request, "core/500.html", context)


class CustomLoginView(auth_views.LoginView):
    """Login screen"""

    template_name = "core/login.html"
    redirect_authenticated_user = True

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""

        user_app = {
            "bt": "bartender",
            "ct": "customer",
            "wt": "bartender",
        }

        has_role = (
            self.request.user.role if self.request.user.is_anonymous is False else None
        )
        if has_role:
            redirect_to = f"../../{user_app[has_role]}/"
            if has_role == "ct" and not self.request.user.customer_table:
                redirect_to += "set_table"
        else:
            redirect_to = ""

        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )

        return redirect_to if url_is_safe else ""


class ChangePasswordView(auth_views.PasswordChangeView):
    template_name = "core/change_password.html"
    form_class = CustomChangePasswordForm
    success_url = reverse_lazy("core:change_password")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx["base"] = "core/base.html"
        if self.request.user.is_customer:
            ctx["base"] = "customer/base.html"
        elif self.request.user.is_bartender:
            ctx["base"] = "bartender/base.html"

        return ctx

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Hasło zostało zmienione.")

        return super().form_valid(form)
