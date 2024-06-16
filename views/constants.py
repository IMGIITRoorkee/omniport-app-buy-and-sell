from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from buy_and_sell import constants
from buy_and_sell.serializers.constants import ConstantSerializer

class ConstantViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    List view for constants and their codes
    """
    renderer_classes = [JSONRenderer,]
    serializer_class = ConstantSerializer

    def list(self, request):
        """
        Return JSONified dictionary of constants and corresponding codes.
        :return: dictionay of contants and codes
        """
        mapping = constants.PERIODICITY_MAP
        reverse_periodicity_map = \
            {mapping[key]: key for key in mapping.keys()}
        response ={}
        response['periodicity']=reverse_periodicity_map

        return Response(response)