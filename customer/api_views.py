from django.http import JsonResponse
from rest_framework.views import APIView
from rules.contrib.views import PermissionRequiredMixin

from core.models import DrinkQueue, Drink


class OrderDrinkApiView(PermissionRequiredMixin, APIView):
    """Api endpoint for customer drink order."""

    permission_required = "customer"

    def post(self, request):
        """Create drink order and return status success."""

        drink_id = request.data["drink_id"]
        user = request.user
        drink = Drink.objects.get(pk=drink_id)
        user_drink_orders = DrinkQueue.objects.filter(
            status__in=[
                DrinkQueue.DrinkQueueStatus.CREATED,
                DrinkQueue.DrinkQueueStatus.ACCEPTED,
                DrinkQueue.DrinkQueueStatus.IN_PROGRESS,
            ]
        )
        if user_drink_orders.count() < 4:
            DrinkQueue.objects.create(
                user=user, drink=drink, status=DrinkQueue.DrinkQueueStatus.CREATED
            )
            response_data = {"status": "order_created"}
        else:
            response_data = {"status": "too_many_orders"}
        return JsonResponse(response_data)
