from rest_framework import viewsets

from buy_and_sell.models import PaymentMode
from buy_and_sell.serializers.payment_mode import PaymentModeSerializer

class PaymentModeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple viewset for viewing payment modes available
    """
    queryset = PaymentMode.objects.all()
    serializer_class = PaymentModeSerializer
