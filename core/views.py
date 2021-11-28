from django.shortcuts import render

from Bartender_Assistant.settings import STATIC_ROOT


def home_view(request):
    """Home view"""
    print(STATIC_ROOT)
    return render(request, "core/home.html")
