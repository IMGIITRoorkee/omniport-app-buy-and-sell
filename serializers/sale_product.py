from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from buy_and_sell.models import SaleProduct
from buy_and_sell.serializers.payment_mode import PaymentModeSerializer

class SaleProductSerializer(serializers.ModelSerializer):
    """
    Serializer to serialize the sale product model
    """    
    class Meta:
        """
        Details of the fields included in the serializer
        """
        model = SaleProduct
        fields = ('id', 'person', 'name', 'cost', 'category', 'datetime_created',
        'start_date', 'end_date', 'is_phone_visible', 'details',
        'warranty_detail', 'payment_modes'
        )
        read_only_fields = ('datetime_created', 'start_date', 'person')
    
    def validate_category(self, value):
        """
        Custom validation for the category field
        """
        if value is None:
            raise serializers.ValidationError('NULL value for this field '+
            'is not allowed')
        return value

    def create(self, validated_data):
        """
        Create model instance with person for request
        """
        person = self.context['request'].person
        validated_data['person'] = person
        return super().create(validated_data)
