from rest_framework import serializers

from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer to serialize category model
    """

    sub_categories = serializers.SerializerMethodField()

    def get_sub_categories(self, obj):
        return [
            CategorySerializer(category).data
            for category in obj.get_descendants(include_self=False)
        ]

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
            'sub_categories'
        )
