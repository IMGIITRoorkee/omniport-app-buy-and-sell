from datetime import date
from datetime import datetime

from rest_framework import serializers

from kernel.managers.get_role import get_all_roles
from kernel.serializers.person import PersonSerializer
from kernel.serializers.roles.student import StudentSerializer
from kernel.serializers.roles.faculty_member import FacultyMemberSerializer
from kernel.serializers.generics.contact_information import ContactInformationSerializer

from buy_and_sell.models import SaleProduct
from buy_and_sell.serializers.payment_mode import PaymentModeSerializer
from buy_and_sell.serializers.picture import PictureSerializer
from buy_and_sell.serializers.categories import CategorySerializer

class SaleProductSerializer(serializers.ModelSerializer):
    """
    Serializer to serialize the sale product model
    """
    
    pictures = serializers.SerializerMethodField()
    person = serializers.SerializerMethodField()
    payment_modes = PaymentModeSerializer(
        many=True,
        read_only=True,
    )
    category = CategorySerializer(
        style={
            'base_template':'fieldset.html',
        }
    )

    def get_payment_modes(self, obj):
        return [PaymentModeSerializer(x) for x in obj.payment_modes]

    def get_pictures(self, obj):
        return [x.picture.url for x in obj.picture_set.all()] 
    
    def get_person(self, obj):

        roles = get_all_roles(obj.person)
        
        try:
            contact_information = obj.person.contact_information.get()
        except:
            contact_information = None
        person = None

        if "Student" in roles:
            person = StudentSerializer(
                obj.person.student_set.get()
            ).data
        elif "FacultyMember" in roles:
            person = FacultyMemberSerializer(
                obj.person.facultymember_set.get()
            ).data

        contact_information = ContactInformationSerializer(
            contact_information
        ).data   

        if(obj.is_phone_visible == False):
            contact_information.pop('primary_phone_number')
            contact_information.pop('secondary_phone_number')            
    
        person['person']['contact_information'] = contact_information

        return person

    class Meta:
        """
        Details of the fields included in the serializer
        """
        model = SaleProduct
        fields = ('id', 'name', 'cost', 'category', 'datetime_created',
        'start_date', 'end_date', 'is_phone_visible', 'details',
        'warranty_detail', 'payment_modes', 'pictures', 'person'
        )
        read_only_fields = ('datetime_created', 'start_date', 'person',)
    
    def validate_category(self, value):
        """
        Custom validation for the category field
        """
        if value is None:
            raise serializers.ValidationError('NULL value for this field '+
            'is not allowed')
        return value
    
    def validate_end_date(self, value):
        """
        Custom validation for the end_date field
        """
        if isinstance(value, date):
            if (value <= datetime.now().date()):
                raise serializers.ValidationError('End date can not be '+
                'in the past.')
            return value
        else:
            raise serializers.ValidationError('End date can not be '+
                'blank.')


    def create(self, validated_data):
        """
        Create model instance with person from request.
        """
        person = self.context['request'].person
        validated_data['person'] = person
        return super().create(validated_data)
