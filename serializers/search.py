from rest_framework import serializers

from buy_and_sell.models import SaleProduct
from buy_and_sell.models import RequestProduct
from buy_and_sell.serializers.sale_product import SaleProductSerializer
from buy_and_sell.serializers.request_product import RequestProductSerializer

class GlobalSearchSerializer(serializers.ModelSerializer):
    """
    Serializer to serialize the search results
    """

    class Meta:
        model = SaleProduct

    def to_representation(self, obj):
        if isinstance(obj, SaleProduct):
            serializer = SaleProductSerializer(obj)
        elif isinstance(obj, RequestProduct):
            serializer = RequestProductSerializer(obj)
        else:
            raise Exception("No results!")
        return serializer.data
