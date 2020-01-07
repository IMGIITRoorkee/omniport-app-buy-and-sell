import datetime
import logging
from django.contrib.contenttypes.models import ContentType

from rest_framework import viewsets
from rest_framework import generics

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from categories.models import Category

from notifications.actions import push_notification

from feed.models import Bit

from buy_and_sell.models import RequestProduct, SaleProduct
from buy_and_sell.serializers.request_product import RequestProductSerializer
from buy_and_sell.permissions.is_owner_or_read_only import IsOwnerOrReadOnly


class RequestProductList(generics.ListAPIView):
    """
    View to list request products on the basis of category.
    """

    serializer_class = RequestProductSerializer

    def get_queryset(self):

        request_arg = self.kwargs['argument']
        if(request_arg):
            if request_arg == "my_products":
                return RequestProduct.objects.filter(
                    person=self.request.person,
                    end_date__gte=datetime.date.today()
                ).order_by('-id')
            else:
                try:
                    parent_category = Category.objects.get(slug=request_arg)
                except Category.DoesNotExist:
                    return RequestProduct.objects.none()

                sub_categories = parent_category.get_descendants(
                    include_self=True
                ).order_by('-id')
                return RequestProduct.objects.filter(
                    category__in=sub_categories,
                    end_date__gte=datetime.date.today()
                ).order_by('-id')
        else:
            return RequestProduct.objects.filter(
                end_date__gte=datetime.date.today()
            ).order_by('-id')


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
    ).order_by('-id')
    serializer_class = RequestProductSerializer

    def perform_create(self, serializer):
        request_product = serializer.save()

        corresponding_sale_items = SaleProduct.objects.filter(category = request_product.category)
        corresponding_persons = corresponding_sale_items.values_list('person', flat=True).distinct()
        if(corresponding_persons is not None):
            push_notification(
                template = request_product.name,
                category = request_product.category,
                has_custom_users_target = True,
                persons = list(corresponding_persons)
            )
            
        bit = Bit()
        bit.app_name = 'buy_and_sell'
        bit.entity = request_product
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
