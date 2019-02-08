from datetime import datetime

from rest_framework import serializers

from kernel.managers.get_role import get_all_roles
from kernel.serializers.roles.student import StudentSerializer
from kernel.serializers.roles.faculty_member import FacultyMemberSerializer
from kernel.serializers.generics.contact_information import (
    ContactInformationSerializer,
)

from categories.models import Category

from buy_and_sell.models import SaleProduct
from buy_and_sell.models import PaymentMode

from buy_and_sell.serializers.payment_mode import PaymentModeSerializer
from buy_and_sell.serializers.picture import PictureSerializer
from buy_and_sell.serializers.categories import CategorySerializer


class SaleProductSerializer(serializers.ModelSerializer):
    """
    Serializer to serialize the Person model
    """

    class Meta:
        """
        Details of the fields included in the serializer
        """

        read_only_fields = "__all__"
