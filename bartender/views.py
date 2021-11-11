from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import (
    DrinkSerializer,
    IngredientStorageSerializer,
    IngredientNeededSerializer,
    DrinkQueueSerializer,
    EarningsSerializer,
    UserSerializer,
)
from core.models import (
    Drink,
    IngredientStorage,
    IngredientNeeded,
    DrinkQueue,
    Earnings,
    User,
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DrinkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = (
        Drink.objects.all()
        .prefetch_related("ingredient_needed", "ingredient_needed__storage_ingredient")
        .order_by("name")
    )
    serializer_class = DrinkSerializer
    ordering_fields = [
        "name",
    ]
    filterset_fields = [
        "name",
        "is_possible_to_make",
        "complicated",
        "price",
        "ingredient_needed__storage_ingredient",
    ]


class IngredientStorageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = IngredientStorage.objects.all()
    serializer_class = IngredientStorageSerializer
    ordering_fields = [
        "name",
    ]
    filterset_fields = [
        "name",
        "type",
    ]


class IngredientNeededViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = IngredientNeeded.objects.all()
    serializer_class = IngredientNeededSerializer
    ordering_fields = ["storage_ingredient__name", "amount"]
    filterset_fields = [
        "drink__name",
        "storage_ingredient__name",
        "storage_ingredient__type",
        "amount",
        "is_enough_to_make_drink",
    ]


class DrinkQueueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = (
        DrinkQueue.objects.all()
        .select_related("user", "drink")
        .prefetch_related(
            "drink__ingredient_needed", "drink__ingredient_needed__storage_ingredient"
        )
    )
    serializer_class = DrinkQueueSerializer
    ordering_fields = [
        "order_date",
    ]
    filterset_fields = [
        "user__username",
        "drink__name",
        "status",
    ]


class EarningsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Earnings.objects.all()
    serializer_class = EarningsSerializer
    ordering_fields = [
        "sum_date",
    ]
