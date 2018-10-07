import ipdb

from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action

from categories.models import Category
from buy_and_sell.models import SaleProduct
from buy_and_sell.models import Picture
from buy_and_sell.serializers.picture import PictureSerializer
from buy_and_sell.serializers.sale_product import SaleProductSerializer
from buy_and_sell.permissions.is_owner_or_read_only import IsOwnerOrReadOnly

class SaleProductList(generics.ListAPIView):
    """
    View to list the products for sale based on category and
    owner of the product
    """

    serializer_class = SaleProductSerializer
    
    def get_queryset(self):
        """
        Dynamically set the queryset
        """
        request_arg = self.kwargs['argument']
        if(request_arg):
            if (request_arg == "my_products"):
                return SaleProduct.objects.filter(person=self.request.person)
            else:
                try:
                    parent_category = Category.objects.get(name=request_arg)
                except:
                    return SaleProduct.objects.none()
                
                decendent_categories = parent_category.get_descendants(
                    include_self=True
                )
                return SaleProduct.objects.filter(
                    category__in = decendent_categories
                )
        else:
            return SaleProduct.objects.all()


class SaleProductViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet to list, detail, add, edit and delete the sale products
    """
    authentication_classes = (
        SessionAuthentication,
    )
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )
    queryset = SaleProduct.objects.all()
    serializer_class = SaleProductSerializer
    
    def get_serializer_context(self):
        """
        Pass the request to serializer
        """
        return {'request': self.request}
    
    def update(self, request, *args, **kwargs):
        """
        Create Picture instance for the product.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        pictureFile = request.FILES['picture']
        picture = PictureSerializer(
            data={
                'product':instance.id,
                'picture':pictureFile
            }
        )
        picture.is_valid(
            raise_exception=True
        )
        picture.save()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(
            raise_exception=True
        )
        self.perform_update(serializer)
