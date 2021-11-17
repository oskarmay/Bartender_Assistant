from rest_framework import serializers
from core.models import (
    Drink,
    IngredientStorage,
    IngredientNeeded,
    DrinkQueue,
    Earnings,
    User,
)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            "url",
            "username",
            "password",
            "one_use_account_password",
            "first_name",
            "last_name",
            "role",
            "expire_date",
        )
        # read_only_fields = ('username', 'password', 'one_use_account_password', 'first_name', 'last_name', 'role', 'expire_date')


class DrinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Drink
        fields = (
            "url",
            "name",
            "is_possible_to_make",
            "complicated",
            "price",
            "date_creation",
            "date_modified",
            "ingredient_needed",
        )
        read_only_fields = ("is_possible_to_make",)


class IngredientStorageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IngredientStorage
        fields = ("url", "name", "type", "unit", "storage_amount")


class IngredientNeededSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = IngredientNeeded
        fields = (
            "url",
            "drink",
            "storage_ingredient",
            "amount",
            "is_enough_to_make_drink",
        )


class DrinkQueueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DrinkQueue
        fields = ("url", "user", "drink", "status", "order_date")


class EarningsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Earnings
        fields = ("url", "sum_date", "sum")
        # read_only_fields = ('sum_date', 'sum')
