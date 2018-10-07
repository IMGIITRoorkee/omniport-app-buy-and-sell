from rest_framework import viewsets

import swapper

from buy_and_sell.serializers.categories import CategorySerializer
from categories.models import Category

class CategoriesViewSet(viewsets.ModelViewSet):
    """
    A simple viewset for viewing Buy and sell Categories
    """
    queryset = Category.objects.filter(
        slug__startswith='buy_and_sell_'
        )
    serializer_class = CategorySerializer
