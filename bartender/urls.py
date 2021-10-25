from django.urls import path, include
from rest_framework import routers
from .views import DrinkViewSet, IngredientStorageViewSet, IngredientNeededViewSet, DrinkQueueViewSet, EarningsViewSet, \
    UserViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'drinks', DrinkViewSet)
router.register(r'ingredient storage', IngredientStorageViewSet)
router.register(r'ingredient needed', IngredientNeededViewSet)
router.register(r'drink queue', DrinkQueueViewSet)
router.register(r'earnings', EarningsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
