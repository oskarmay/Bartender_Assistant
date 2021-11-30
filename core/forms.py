from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import ugettext_lazy as _

from core.models import User


class CustomChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
        label=_(u"Old password"),
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
        label=_(u"New password"),
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "type": "password"}),
        label=_(u"Repeat new password"),
    )

    class Meta:
        model = User
        fields = ("old_password", "new_password1", "new_password2")
