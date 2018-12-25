from rest_framework import generics

from buy_and_sell.models import Picture
from buy_and_sell.serializers.picture import PictureSerializer

class PicturesList(generics.ListCreateAPIView):
    """
    Viewset to list pictures of all the products
    """
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
