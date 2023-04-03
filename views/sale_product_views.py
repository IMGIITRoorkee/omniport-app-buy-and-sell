import datetime
import logging
from django.contrib.contenttypes.models import ContentType

from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from categories.models import Category

from notifications.actions import push_notification
from emails.actions import email_push

from feed.models import Bit

from buy_and_sell.models import SaleProduct, RequestProduct
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

        request_arg = self.kwargs.get('argument', '')
        filter_arg = self.kwargs.get('filter_slug', '')

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
                    logger.error(
                        f'{self.request.person} put a product to sale but the parent'
                        f' category with slug \'{request_arg}\' does not exist '
                    )
                    return SaleProduct.objects.none()

                sub_categories = parent_category.get_descendants(
                    include_self=True
                )

                if(filter_arg=="for_rent"):
                    return SaleProduct.objects.filter(
                        category__in=sub_categories,
                        end_date__gte=datetime.date.today(),
                        is_rental=True,
                    ).order_by('-id')

                elif( filter_arg=="for_sale"):
                    return SaleProduct.objects.filter(
                        category__in=sub_categories,
                        end_date__gte=datetime.date.today(),
                        is_rental=False,
                    ).order_by('-id')

                return SaleProduct.objects.filter(
                    category__in=sub_categories,
                    end_date__gte=datetime.date.today(),
                ).order_by('-id')
                
        else:
            if(filter_arg=="for_rent"):
                return SaleProduct.objects.filter(
                    end_date__gte=datetime.date.today(),
                    is_rental=True,
                ).order_by('-id')
            
            elif(filter_arg=="for_sale"):
                return SaleProduct.objects.filter(
                    end_date__gte=datetime.date.today(),
                    is_rental=False,
                ).order_by('-id')
            
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
        if sale_product.is_rental:
            product_type = 'rent'
        else:
            product_type = 'sale'
        
        logger.info(f'{sale_product.name} was added for {product_type} by {self.request.person}')
        persons_to_be_notified = RequestProduct.objects.filter(category = sale_product.category).values_list('person', flat=True).distinct()
        if persons_to_be_notified.exists():
            push_notification(
                template = f'{sale_product.name} was added for {product_type}',
                category = sale_product.category,
                has_custom_users_target = True,
                persons = list(persons_to_be_notified),
                send_only_to_subscribed_users = True
            )
            email_push(
                subject_text = f'The item, {sale_product.name}, requested by you has a prospective seller on Buy and Sell!',
                body_text = f'{sale_product.name} was added for {product_type} by {sale_product.person.full_name}.'
                            f' You can contact them by mailing them at { sale_product.person.contact_information.first().email_address}.'
                            f'\n\n Note: If the  phone number or email id of the seller is missing, that means that { sale_product.person.full_name } '
                            f' has not filled in their contact information in the channel-i database ',
                category = sale_product.category,
                has_custom_user_target = True,
                persons = list(persons_to_be_notified),
                send_only_to_subscribed_users = True
            )
            logger.info(
                f'{self.request.person} put a product to {product_type}. '
                f'Notifications and emails were dispatched for '
                f'{sale_product.category}'
            )

        bit = Bit()
        bit.app_name = 'buy_and_sell'
        bit.entity = sale_product
        bit.save()

    def perform_destroy(self, instance):
        item_type = ContentType.objects.get_for_model(instance)
        logger.info(f'{instance} was deleted by {self.request.person}')
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
