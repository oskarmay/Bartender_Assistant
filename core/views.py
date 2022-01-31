from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.forms import CustomChangePasswordForm
from core.models import User


class HomeTemplateView(TemplateView):
    """View of Home template view"""

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
    if request.user.is_anonymous:
        base = "core/base.html"
    elif request.user.is_customer:
        base = "customer/base.html"
    elif request.user.is_bartender:
        base = "bartender/base.html"
    else:
        base = "core/base.html"

    context = {"base_template": base}
    return render(request, "core/404.html", context)


def error_500(request):
    if request.user.is_anonymous:
        base = "core/base.html"
    elif request.user.is_customer:
        base = "customer/base.html"
    elif request.user.is_bartender:
        base = "bartender/base.html"
    else:
        base = "core/base.html"

    context = {"base_template": base}
    return render(request, "core/500.html", context)


class CustomLoginView(auth_views.LoginView):
    """View of login screen."""

    template_name = "core/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Check if user account should be active."""
        user_trying_to_login = User.objects.get(username=form.cleaned_data["username"])

        user_active = user_trying_to_login.is_expired

        if user_active:
            messages.error(self.request, "Konto nie jest już aktywne.")
            return redirect(reverse_lazy("core:login"))
        return super().form_valid(form)

    def get_success_url(self):
        """Redirection to the home page of the logged in user."""

        if self.request.user.is_anonymous:
            return reverse_lazy("core:home")
        elif self.request.user.is_customer:
            if not self.request.user.customer_table:
                return reverse_lazy("customer:set_table")
            return reverse_lazy("customer:home")
        elif self.request.user.is_bartender:
            return reverse_lazy("bartender:home")
        else:
            return reverse_lazy("core:home")


class ChangePasswordView(auth_views.PasswordChangeView):
    """View of account password change."""

    template_name = "core/change_password.html"
    form_class = CustomChangePasswordForm
    success_url = reverse_lazy("core:change_password")

    def get_context_data(self, **kwargs):
        """Add base template to ctx."""

        ctx = super().get_context_data()
        ctx["base"] = "core/base.html"
        if self.request.user.is_customer:
            ctx["base"] = "customer/base.html"
        elif self.request.user.is_bartender:
            ctx["base"] = "bartender/base.html"

        return ctx

    def form_valid(self, form):
        """Add information about password changing"""

        form.save()
        messages.success(self.request, "Hasło zostało zmienione.")

        return super().form_valid(form)
