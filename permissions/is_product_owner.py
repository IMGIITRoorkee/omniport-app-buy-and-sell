from rest_framework import permissions

from buy_and_sell.models import SaleProduct


def has_product_permission(object_id, person):
    sale_product = SaleProduct.objects.get(pk=object_id)
    return sale_product.person == person
