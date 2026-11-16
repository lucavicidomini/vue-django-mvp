from rest_framework import serializers
from fuels.models import Fuel
from shared.fuel_type_constants import FUEL_TYPE_CHOICES

class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuel
        fields = '__all__'
        read_only_fields = ['id']

