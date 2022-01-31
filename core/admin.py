from django.contrib import admin
from django.contrib.admin import display
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import pgettext_lazy

from core.models import (
    Drink,
    Earnings,
    IngredientNeeded,
    IngredientStorage,
    Orders,
    User,
)


@admin.register(User)
class UserAdmin(UserAdmin):
    """
    Admin for Custom User
    """

    fieldsets = (
        (None, {"fields": ("username", "email", "password", "role")}),
        (
            ("User Permission"),
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
        (
            ("User info"),
            {
                "classes": ("collapse",),
                "fields": (
                    "first_name",
                    "last_name",
                ),
            },
        ),
        (
            ("Customer info"),
            {
                "classes": ("collapse",),
                "fields": (
                    "one_use_account_password",
                    "expire_date",
                ),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "role",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "role",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
    )

    list_filter = (
        "is_staff",
        "role",
        "is_superuser",
        "is_active",
    )
    list_display_links = ("username",)
    search_fields = (
        "username",
        "role",
        "first_name",
        "last_name",
        "email",
    )
    ordering = ("username", "role", "is_active")


@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "complicated",
        "is_possible_to_make",
        "price",
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
        "price",
        "is_possible_to_make",
        "date_creation",
        "date_modified",
    )


@admin.register(IngredientStorage)
class IngredientStorageAdmin(admin.ModelAdmin):
    fields = ("name", "type", "unit", "storage_amount", "image")
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


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    fields = (
        "user",
        "drink",
        "storage_order",
        "status",
    )
    readonly_fields = ("order_date",)
    list_display = (
        "user",
        "drink",
        "storage_order",
        "status",
        "order_date",
    )
    list_filter = (
        "user",
        "drink",
        "storage_order",
        "status",
        "order_date",
    )

    # @display(ordering="drink__name")
    # def get_drink_name(self, obj):
    #     return obj.drink.name


@admin.register(Earnings)
class EarningsAdmin(admin.ModelAdmin):
    fields = (
        "sum_date",
        "sum",
    )
    readonly_fields = (
        "sum_date",
        "sum",
    )
    list_display = (
        "sum_date",
        "sum",
    )
