from django import forms

from core.models import IngredientStorage


class IngredientCreateForm(forms.ModelForm):
    """Digital type creation form"""

    class Meta:
        model = IngredientStorage
        fields = ["name", "type", "unit", "storage_amount", "image"]
        label = {
            "name": ("Nazwa"),
            "type": ("Typ"),
            "unit": ("Jednostka"),
            "image": ("Zdjęcie"),
            "storage_amount": ("Liczba w magazynie"),
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "type": forms.Select(
                choices=IngredientStorage.Types.choices, attrs={"class": "form-control"}
            ),
            "unit": forms.Select(
                choices=IngredientStorage.Units.choices, attrs={"class": "form-control"}
            ),
            "storage_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
        }
