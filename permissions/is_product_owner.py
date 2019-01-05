from rest_framework import permissions

from buy_and_sell.models import SaleProduct

class IsProductOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of a product to add images to it.
    """

    def has_object_permission(self, request, view, obj):
        object_id = request.data['product']  
        sale_product = SaleProduct.objects.get(pk=object_id)
        
        return sale_product.person == request.person
