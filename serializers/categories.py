from rest_framework import serializers

from categories.models import Category

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer to serialize category model
    """
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'level',
            'parent'
        )
        read_only_fields = (
            'id',
            'name',
            'slug',
            'level',
            'parent'
        )
