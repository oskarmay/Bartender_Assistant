from django.contrib import admin
from django.contrib.admin import display
from django.utils.translation import pgettext_lazy

from core.models import (
    Drink,
    DrinkQueue,
    IngredientNeeded,
    IngredientStorage,
)


@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "complicated",
        "is_possible_to_make",
        "date_creation",
        "date_modified",
    )
    readonly_fields = (
        "is_possible_to_make",
        "date_creation",
        "date_modified",
    )
    list_display = (
        "name",
        "complicated",
        "is_possible_to_make",
        "date_creation",
        "date_modified",
    )


@admin.register(IngredientStorage)
class IngredientStorageAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "type",
        "unit",
        "storage_amount",
    )
    list_display = (
        "name",
        "type",
        "storage_amount",
        "unit",
    )


@admin.register(IngredientNeeded)
class IngredientNeededStorageAdmin(admin.ModelAdmin):
    fields = (
        "drink",
        "storage_ingredient",
        "amount",
        "is_enough_to_make_drink",
    )
    readonly_fields = ("is_enough_to_make_drink",)
    list_display = (
        "get_ingredient_name",
        "storage_ingredient",
        "get_drink_complicated",
        "get_ingredient_type",
        "is_enough_to_make_drink",
        "amount",
        "get_ingredient_unit",
    )

    @display(
        ordering="ingredient_storage__name",
        description=pgettext_lazy("ingredient_storage", "name"),
    )
    def get_ingredient_name(self, obj):
        return obj.storage_ingredient.name

    @display(
        ordering="ingredient_storage__unit",
        description=pgettext_lazy("ingredient_storage", "unit"),
    )
    def get_ingredient_unit(self, obj):
        return obj.storage_ingredient.get_unit_display()

    @display(
        ordering="ingredient_storage__type",
        description=pgettext_lazy("ingredient_storage", "type"),
    )
    def get_ingredient_type(self, obj):
        return obj.storage_ingredient.get_type_display()

    @display(
        ordering="drink__name",
        description=pgettext_lazy("drink", "name"),
    )
    def get_drink_name(self, obj):
        return obj.drink.name

    @display(
        ordering="drink__complicated",
        description=pgettext_lazy("drink", "complicated"),
    )
    def get_drink_complicated(self, obj):
        return obj.drink.get_complicated_display()


@admin.register(DrinkQueue)
class DrinkQueueAdmin(admin.ModelAdmin):
    fields = (
        "user",
        "drink",
        "status",
    )
    list_display = (
        "user",
        "drink",
        "status",
    )
    list_filter = (
        "user",
        "drink",
        "status",
    )

    # @display(ordering="drink__name")
    # def get_drink_name(self, obj):
    #     return obj.drink.name
