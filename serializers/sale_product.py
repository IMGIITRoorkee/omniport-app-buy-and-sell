from datetime import date
from datetime import datetime

from rest_framework import serializers

from formula_one.models import ContactInformation
from kernel.managers.get_role import get_all_roles
from kernel.serializers.roles.student import StudentSerializer
from kernel.serializers.roles.faculty_member import FacultyMemberSerializer
from formula_one.serializers.generics.contact_information import (
    ContactInformationSerializer,
)
from buy_and_sell.constants import LIFESPAN
from categories.models import Category
from buy_and_sell.models import SaleProduct
from buy_and_sell.models import PaymentMode


class SaleProductSerializer(serializers.ModelSerializer):
    """
    Serializer to serialize the sale product model
    """

    pictures = serializers.SerializerMethodField()
    person = serializers.SerializerMethodField()
    payment_modes = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=PaymentMode.objects.all()
    )
    category = serializers.SlugRelatedField(
        many=False,
        queryset=Category.objects.filter(
            slug__startswith='buy_and_sell_'
        ),
        slug_field='slug'
    )

    def get_pictures(self, obj):
        return [x.picture.url for x in obj.picture_set.all()]

    def get_person(self, obj):

        roles = get_all_roles(obj.person)

        try:
            contact_information = obj.person.contact_information.get()
        except ContactInformation.DoesNotExist:
            contact_information = None
        person = None

        if "Student" in roles:
            person = StudentSerializer(
                obj.person.student
            ).data
        elif "FacultyMember" in roles:
            person = FacultyMemberSerializer(
                obj.person.facultymember
            ).data

        contact_information = ContactInformationSerializer(
            contact_information
        ).data

        if obj.is_phone_visible is False:
            contact_information.pop('primary_phone_number')
            contact_information.pop('secondary_phone_number')

        if person:
            person['person']['contact_information'] = contact_information

        return person

    class Meta:
        """
        Details of the fields included in the serializer
        """

        model = SaleProduct
        fields = ('id', 'name', 'cost', 'category', 'datetime_created',
                  'start_date', 'end_date', 'is_phone_visible', 'is_rental', 'details',
                  'warranty_detail', 'payment_modes', 'pictures', 'person', 
                  'security_deposit', 'periodicity',
                  )
        read_only_fields = ('datetime_created', 'start_date', 'person',)

    def validate_category(self, value):
        """
        Custom validation for the category field
        """
        if value is None:
            raise serializers.ValidationError('NULL value for this field ' +
                                              'is not allowed')
        elif not value.slug.startswith('buy_and_sell_'):
            raise serializers.ValidationError('Invalid category')
        return value

    def validate_end_date(self, value):
        """
        Custom validation for the end_date field
        """

        if isinstance(value, date):
            if (value <= datetime.now().date()):
                raise serializers.ValidationError('End date can not be ' +
                                                  'in the past.')
            return value
        else:
            raise serializers.ValidationError('End date can not be ' +
                                              'blank.')

    def validate(self, data):
        if data['is_rental'] is False:
            if data['security_deposit']>0:
                raise serializers.ValidationError('Sale product cannot have' +
                                                 ' a security deposit.')
            if data['periodicity'] is not LIFESPAN:
                raise serializers.ValidationError('Invalid periodicity for Sale' +
                                                 ' product.')
        else:
            if data['periodicity'] is LIFESPAN:
                raise serializers.ValidationError('Invalid periodicity for Rental' +
                                                 ' product.')
        
        if data['security_deposit']<0:
            raise serializers.ValidationError('Security deposit cannot' +
                                                 ' be negative.')

        return data

            
    def create(self, validated_data):
        """
        Create model instance with person from request.
        """

        person = self.context['request'].person
        validated_data['person'] = person
        return super().create(validated_data)
