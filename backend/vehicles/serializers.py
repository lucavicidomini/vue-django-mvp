from rest_framework import serializers
from vehicles.models import Vehicle, VehicleScenario, VehicleRechargeSpeed, FUEL_TYPE_CHOICES

class VehicleScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleScenario
        fields = '__all__'

class VehicleRechargeSpeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleRechargeSpeed
        fields = '__all__'

class VehicleRechargeSpeedSyncSerializer(VehicleRechargeSpeedSerializer):
    # Make id writeable, so it can be updated during sync operations
    id = serializers.IntegerField(min_value=0)

    # Hide vehicle field during sync operations: will be enforced by owner entity
    class Meta(VehicleRechargeSpeedSerializer.Meta):
        fields = ['id', 'name', 'net_speed', 'gross_speed']

class VehicleScenarioSyncSerializer(VehicleScenarioSerializer):
    id = serializers.IntegerField(min_value=0)

    class Meta(VehicleScenarioSerializer.Meta):
        fields = ['id', 'name', 'consumption']

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class VehicleDetailSerializer(VehicleSerializer):
    # Always include relationships, even for lists
    # (Yes, may not be performant in real-world production scenarios)
    scenarios = VehicleScenarioSerializer(
        source='vehiclescenario_set', many=True, read_only=True
    )
    recharge_speeds = VehicleRechargeSpeedSerializer(
        source='vehiclerechargespeed_set', many=True, read_only=True
    )

    class Meta(VehicleSerializer.Meta):
        fields = ['id', 'name', 'usable_battery', 'fuel_type', 'scenarios', 'recharge_speeds']

