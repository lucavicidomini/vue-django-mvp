from django.db import models

class Fuel(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    unit = models.CharField(max_length=5)
