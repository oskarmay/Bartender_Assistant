from django import forms

from core.models import Drink, IngredientNeeded, IngredientStorage


class IngredientStorageForm(forms.ModelForm):
    """Ingredient Storage creation form"""

    class Meta:
        model = IngredientStorage
        fields = [
            "name",
            "type",
            "unit",
            "storage_amount",
            "price",
            "has_alcohol",
            "can_be_ordered",
            "image",
        ]
        label = {
            "name": ("Nazwa"),
            "type": ("Typ"),
            "unit": ("Jednostka"),
            "image": ("Zdjęcie"),
            "storage_amount": ("Liczba w magazynie"),
            "price": ("Cena"),
            "has_alcohol": ("Posiada alkohol?"),
            "can_be_ordered": ("Do zamówienia?"),
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
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "has_alcohol": forms.CheckboxInput(attrs={"class": "form-control"}),
            "can_be_ordered": forms.CheckboxInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control form-control-sm"}
            ),
        }


class DrinkForm(forms.ModelForm):
    """Drink creation form"""

    class Meta:
        model = Drink
        fields = [
            "name",
            "type",
            "complicated",
            "amount",
            "price",
            "image",
            "preparation_description",
        ]
        label = {
            "name": ("Nazwa"),
            "type": ("Typ"),
            "complicated": ("Skomplikowanie"),
            "amount": ("Ilość"),
            "price": ("Cena"),
            "image": ("Zdjęcie"),
            "preparation_description": ("Opis"),
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "type": forms.Select(
                choices=Drink.Types.choices, attrs={"class": "form-control"}
            ),
            "complicated": forms.Select(
                choices=Drink.ComplicatedLevels.choices, attrs={"class": "form-control"}
            ),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control form-control-sm"}
            ),
            "preparation_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "cols": 1000,
                    "max-length": 2048,
                }
            ),
        }


class IngredientNeededForm(forms.ModelForm):
    """Ingredient Needed for drink creation form"""

    class Meta:
        model = IngredientNeeded

        fields = [
            "drink",
            "storage_ingredient",
            "amount",
        ]
        label = {
            "drink": ("Drink"),
            "storage_ingredient": ("Składnik z magazynu"),
            "amount": ("Ilość"),
        }
        widgets = {
            "drink": forms.Select(attrs={"class": "form-control"}),
            "storage_ingredient": forms.Select(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
        }
