from rest_framework import serializers

from buy_and_sell.models import Picture


class PictureSerializer(serializers.ModelSerializer):
    """
    Serializer to serialize picture model
    """

    class Meta:
        model = Picture
        fields = '__all__'
