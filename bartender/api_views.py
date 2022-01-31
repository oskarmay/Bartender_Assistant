from django.http import JsonResponse
from rest_framework.views import APIView
from rules.contrib.views import PermissionRequiredMixin

from core.models import Orders


class RejectOrderApiView(PermissionRequiredMixin, APIView):
    """Api endpoint for bartender reject orders."""

    permission_required = "is_in_staff"

    def post(self, request):
        """Reject ordered orders and return result status."""

        order_id = request.data["order_id"]
        try:
            ordered_drink = Orders.objects.get(id=order_id)
            ordered_drink.set_rejected()
            response_data = {"status": "order_rejected"}
        except Orders.DoesNotExist:
            response_data = {"status": "does_not_exist"}

        return JsonResponse(response_data)


class AcceptOrderApiView(PermissionRequiredMixin, APIView):
    """Api endpoint for bartender accept orders."""

    permission_required = "is_in_staff"

    def post(self, request):
        """Accept ordered orders and return result status."""

        order_id = request.data["order_id"]
        try:
            ordered_drink = Orders.objects.get(id=order_id)

            if ordered_drink.is_created:
                ordered_drink.set_accepted()
                response_data = {"status": "order_accepted"}
            else:
                response_data = {"status": "bad_order_status_for_this_action"}
        except Orders.DoesNotExist:
            response_data = {"status": "does_not_exist"}

        return JsonResponse(response_data)


class SetInProgressOrderApiView(PermissionRequiredMixin, APIView):
    """Api endpoint for bartender set order status to in progress."""

    permission_required = "is_in_staff"

    def post(self, request):
        """Set order status to in progress and return result status."""

        order_id = request.data["order_id"]
        try:
            ordered_drink = Orders.objects.get(id=order_id)
            if ordered_drink.is_accepted:
                ordered_drink.set_in_progress()
                response_data = {"status": "order_in_in_progress"}
            else:
                response_data = {"status": "bad_order_status_for_this_action"}
        except Orders.DoesNotExist:
            response_data = {"status": "does_not_exist"}

        return JsonResponse(response_data)


class CompleteOrderApiView(PermissionRequiredMixin, APIView):
    """Api endpoint for bartender complete order preparation."""

    permission_required = "is_in_staff"

    def post(self, request):
        """Set order status to complete and return result status."""

        order_id = request.data["order_id"]
        try:
            ordered_drink = Orders.objects.get(id=order_id)
            if ordered_drink.is_in_progress:
                ordered_drink.set_completed()
                response_data = {"status": "order_completed"}
            else:
                response_data = {"status": "bad_order_status_for_this_action"}
        except Orders.DoesNotExist:
            response_data = {"status": "does_not_exist"}

        return JsonResponse(response_data)
