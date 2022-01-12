from django.http import JsonResponse
from rest_framework.views import APIView
from rules.contrib.views import PermissionRequiredMixin

from core.models import Drink, Orders


class CreateOrderApiView(PermissionRequiredMixin, APIView):
    """Api endpoint for customer orders order."""

    permission_required = "customer"

    def post(self, request):
        """Create orders order and return result status.."""

        order_id = request.data["order_id"]
        is_drink = request.data["is_drink"]
        user = request.user
        user_orders = Orders.objects.filter(
            status__in=[
                Orders.OrdersStatus.CREATED,
                Orders.OrdersStatus.ACCEPTED,
                Orders.OrdersStatus.IN_PROGRESS,
            ],
            user=user,
        )

        if user_orders.count() < 5:
            if is_drink:
                Orders.objects.create(
                    user=user, drink_id=order_id, status=Orders.OrdersStatus.CREATED
                )
            else:
                Orders.objects.create(
                    user=user,
                    storage_order_id=order_id,
                    status=Orders.OrdersStatus.CREATED,
                )
            response_data = {"status": "order_created"}
        else:
            response_data = {"status": "too_many_orders"}
        return JsonResponse(response_data)


class CancelOrderApiView(PermissionRequiredMixin, APIView):
    """Api endpoint for customer cancel orders ordered."""

    permission_required = "customer"

    def post(self, request):
        """Cancel ordered orders and return result status."""

        ordered_id = request.data["ordered_id"]
        user = request.user
        try:
            ordered_drink = Orders.objects.get(id=ordered_id, user=user)
            if ordered_drink.is_created:
                ordered_drink.set_canceled()
                response_data = {"status": "order_canceled"}
            else:
                response_data = {"status": "too_late_to_cancel_order"}
        except Orders.DoesNotExist:
            response_data = {"status": "does_not_exist"}

        return JsonResponse(response_data)
