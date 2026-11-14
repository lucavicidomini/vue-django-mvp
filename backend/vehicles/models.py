from django.db import models

FUEL_TYPE_CHOICES = [
    (0, 'Electric'),
    (1, 'Petrol'),
    (2, 'Gasoline'),
    (3, 'CNG'), # Compressed Natural Gas (Metano)
    (4, 'LPG'), # Liquefied Petroleum Gas (GPL)
]

class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    usable_battery = models.FloatField()
    fuel_type = models.IntegerField(choices=FUEL_TYPE_CHOICES)

class VehicleScenario(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    consumption = models.FloatField()