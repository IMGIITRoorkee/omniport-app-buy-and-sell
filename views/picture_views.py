from rest_framework import generics
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from buy_and_sell.permissions.is_product_owner import IsProductOwner
from buy_and_sell.models import Picture, SaleProduct
from buy_and_sell.serializers.picture import PictureSerializer

class PicturesList(generics.CreateAPIView):
    """
    View to upload pictures for the products
    """
    
    permission_classes = (
        IsProductOwner,
    )
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

    def create(self, request, *args, **kwargs):
        """
        Create Picture instance for the product.
        """
        objectId = request.data['product']  
        saleProduct = SaleProduct.objects.get( pk=objectId )
        if len(saleProduct.picture_set.all()) < 3:
            return super().create(request,*args, **kwargs)
        else:
            return Response(
                    data={
                    'Error': 'Image was not uploaded as the product already had 3 images.'
                    },
                status=status.HTTP_400_BAD_REQUEST,
                )
            



