import datetime

import logging

from django.contrib.contenttypes.models import ContentType

from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response

from categories.models import Category

from notifications.actions import push_notification
from emails.actions import email_push

from feed.models import Bit

from buy_and_sell.models import SaleProduct, RequestProduct
from buy_and_sell.models import Picture
from buy_and_sell.serializers.picture import PictureSerializer
from buy_and_sell.serializers.sale_product import SaleProductSerializer
from buy_and_sell.permissions.is_owner_or_read_only import IsOwnerOrReadOnly

logger = logging.getLogger("buy_and_sell")

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
                    logger.warning('User tried for a category which does not exist')

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
        logger.info(f'{sale_product.name} was added for class')

        persons_to_be_notified = RequestProduct.objects.filter(category = sale_product.category).values_list('person', flat=True).distinct()
        if persons_to_be_notified.exists():
            push_notification(
                template = f'{sale_product.name} was added for sale',
                category = sale_product.category,
                has_custom_users_target = True,
                persons = list(corresponding_persons)
            )
            email_push(
                subject_text = f'{sale_product.name} was added for sale',
                body_text = f'{sale_product.name} was added for sale',
                category = sale_product.category,
                has_custom_users_target = True,
                persons = list(corresponding_persons)
            )
            logger.info(f'A notification and email was pushed to {sale_product.template}')

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

        logger.info(f'{instance} was deleted')

    def get_serializer_context(self):
        """
        Pass the request to serializer
        """

        return {'request': self.request}
