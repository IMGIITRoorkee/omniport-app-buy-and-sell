from itertools import chain

from rest_framework import generics

from buy_and_sell.serializers.search import GlobalSearchSerializer
from buy_and_sell.models import SaleProduct
from buy_and_sell.models import RequestProduct
 

class GlobalSearchList(generics.ListAPIView):
    """
    View to list the products based on the search query
    """

    serializer_class = GlobalSearchSerializer

    def get_queryset(self):
        """
        Dynamically set the queryset
        """
        
        try:
            query = self.request.query_params.get('query', None)
            sale_product = SaleProduct.objects.filter(name__icontains=query)
            request_product = RequestProduct.objects.filter(name__icontains=query)
            all_results = list(chain(sale_product, request_product))
            all_results.sort(key=lambda x: x.datetime_created)
            return all_results
        except:
            all_results = list()
            return all_results