import datetime

from django.contrib.contenttypes.models import ContentType

from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from categories.models import Category
from feed.models import Bit

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
                return SaleProduct.objects.filter(
                    person=self.request.person,
                    end_date__gte=datetime.date.today()
                ).order_by('-id')
            else:
                try:
                    parent_category = Category.objects.get(slug=request_arg)
                except Category.DoesNotExist:
                    return SaleProduct.objects.none()

                sub_categories = parent_category.get_descendants(
                    include_self=True
                )
                return SaleProduct.objects.filter(
                    category__in=sub_categories,
                    end_date__gte=datetime.date.today()
                ).order_by('-id')
        else:
            return SaleProduct.objects.filter(
                end_date__gte=datetime.date.today()
            ).order_by('-id')


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
    queryset = SaleProduct.objects.filter(
        end_date__gte=datetime.date.today()
    ).order_by('-id')
    serializer_class = SaleProductSerializer

    def perform_create(self, serializer):
        sale_product = serializer.save()

        bit = Bit()
        bit.app_name = 'buy_and_sell'
        bit.entity = sale_product
        bit.save()

    def perform_destroy(self, instance):
        item_type = ContentType.objects.get_for_model(instance)
        bit = Bit.objects.get(
            entity_content_type__pk=item_type.id,
            entity_object_id=instance.id
        )
        bit.delete()
        instance.delete()

    def get_serializer_context(self):
        """
        Pass the request to serializer
        """

        return {'request': self.request}
