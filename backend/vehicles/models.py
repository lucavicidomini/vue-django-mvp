from django.db import models
from shared.fuel_type_constants import FUEL_TYPE_CHOICES

class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    usable_battery = models.FloatField()
    fuel_type = models.IntegerField(choices=FUEL_TYPE_CHOICES)

class VehicleScenario(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    consumption = models.FloatField()

class VehicleRechargeSpeed(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    gross_speed = models.FloatField()
    net_speed = models.FloatField()