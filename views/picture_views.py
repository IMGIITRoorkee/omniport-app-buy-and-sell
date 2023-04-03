from rest_framework import generics
from rest_framework import status

from rest_framework.response import Response

from buy_and_sell.permissions.is_product_owner import has_product_permission
from buy_and_sell.models import Picture, SaleProduct
from buy_and_sell.serializers.picture import PictureSerializer


class PictureList(generics.CreateAPIView):
    """
    View to upload picture for the product
    """

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

    def create(self, request, *args, **kwargs):
        """
        Create Picture instance for the product.
        """

        object_id = request.data['product']
        sale_product = SaleProduct.objects.get(pk=object_id)
        if len(sale_product.picture_set.all()) < 3:
            if has_product_permission(object_id, request.person):
                return super().create(request, *args, **kwargs)
            return Response(
                data={
                    'Error': (
                        'You are not authorized to '
                        'perform this operation'
                    ),
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(
            data={
                'Error': (
                    'Image was not uploaded as the '
                    'product already had 3 images.'
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
