from rest_framework import serializers
from vehicles.models import Vehicle, VehicleScenario, FUEL_TYPE_CHOICES

class VehicleScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleScenario
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class VehicleDetailSerializer(VehicleSerializer):
    scenarios = VehicleScenarioSerializer(
        source='vehiclescenario_set', many=True, read_only=True
    )

    class Meta(VehicleSerializer.Meta):
        fields = ['id', 'name', 'usable_battery', 'fuel_type', 'scenarios']

