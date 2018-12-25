import datetime

from rest_framework import viewsets
from rest_framework import generics

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from categories.models import Category
from buy_and_sell.models import RequestProduct
from buy_and_sell.serializers.request_product import RequestProductSerializer
from buy_and_sell.permissions.is_owner_or_read_only import IsOwnerOrReadOnly


class RequestProductList(generics.ListAPIView):
    """
    View to list requset products on the basis of category.
    """

    serializer_class = RequestProductSerializer
    
    def get_queryset(self):
        
        request_arg = self.kwargs['argument']
        if(request_arg):
            if (request_arg == "my_products"):
                return RequestProduct.objects.filter(person=self.request.person)
            else:
                try:
                    parent_category = Category.objects.get(name=request_arg)
                except:
                    return RequestProduct.objects.none()
                
                decendent_categories = parent_category.get_descendants(
                    include_self=True
                )
                return RequestProduct.objects.filter(
                    category__in = decendent_categories
                )
        else:
            return RequestProduct.objects.all()


class RequestProductViewSet(viewsets.ModelViewSet):

    authentication_classes = (
        SessionAuthentication,
    )
    
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
    
    queryset = RequestProduct.objects.filter(
        end_date__gte=datetime.date.today()
    )
    serializer_class = RequestProductSerializer

    def get_serializer_context(self):
        """
        Pass the request to serializer
        """
        return {'request': self.request}
