from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import DrinkSerializer, IngredientStorageSerializer, IngredientNeededSerializer, DrinkQueueSerializer, \
    EarningsSerializer, UserSerializer
from core.models import Drink, IngredientStorage, IngredientNeeded, DrinkQueue, Earnings, User


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DrinkViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Drink.objects.all().order_by('name')
    serializer_class = DrinkSerializer


class IngredientStorageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = IngredientStorage.objects.all()
    serializer_class = IngredientStorageSerializer


class IngredientNeededViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = IngredientNeeded.objects.all()
    serializer_class = IngredientNeededSerializer


class DrinkQueueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DrinkQueue.objects.all().select_related('user', 'drink')
    serializer_class = DrinkQueueSerializer


class EarningsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Earnings.objects.all()
    serializer_class = EarningsSerializer
