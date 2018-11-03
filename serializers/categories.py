from rest_framework import serializers

from categories.models import Category

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer to serialize category model
    """
    subCategories = serializers.SerializerMethodField()

    def get_subCategories(self, obj):
        return [
            CategorySerializer(x).data for x in obj.get_descendants(include_self=False)
        ]
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'subCategories'
        )
