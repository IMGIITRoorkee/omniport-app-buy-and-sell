from rest_framework import serializers

class ConstantSerializer(serializers.Serializer):
    periodicity = serializers.DictField(child=serializers.CharField())
    
    