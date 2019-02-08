from rest_framework import serializers

from buy_and_sell.models import PaymentMode


class PaymentModeSerializer(serializers.ModelSerializer):
    """
    Serializer to serialize payment mode model
    """

    class Meta:
        model = PaymentMode
        fields = ('id', 'name')
        read_only_fields = ('id', 'name')
