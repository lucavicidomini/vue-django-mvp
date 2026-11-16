from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction

from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from vehicles.models import Vehicle, VehicleScenario
from vehicles.serializers import (
    VehicleSerializer, VehicleScenarioSerializer, VehicleDetailSerializer,
    VehicleScenarioSyncSerializer, VehicleRechargeSpeedSyncSerializer
)

def sync_related_entity(vehicle, related_set, serializer, label):
    if not serializer.is_valid():
        raise ValidationError({label: serializer.errors})

    existing = {related.pk: related for related in related_set.all()}
    related_ids = [item['id'] for item in serializer.validated_data if item['id'] != 0]
    if len(related_ids) != len(set(related_ids)):
        raise ValidationError({label: 'IDs must not be repeated.'})
    if any(related_id not in existing for related_id in related_ids):
        raise ValidationError({label: 'IDs must belong to this vehicle.'})

    related_set.exclude(pk__in=related_ids).delete()
    for related_data in serializer.validated_data:
        related_id = related_data.pop('id')
        if related_id == 0:
            serializer.child.create({**related_data, 'vehicle': vehicle})
        else:
            serializer.child.update(existing[related_id], related_data)

def sync_vehicle_scenarios(vehicle, data):
    serializer = VehicleScenarioSyncSerializer(data=data, many=True)
    sync_related_entity(vehicle, vehicle.vehiclescenario_set, serializer, 'scenarios')

def sync_vehicle_recharge_speeds(vehicle, data):
    serializer = VehicleRechargeSpeedSyncSerializer(data=data, many=True)
    sync_related_entity(vehicle, vehicle.vehiclerechargespeed_set, serializer, 'recharge_speeds')

@api_view(['GET', 'POST'])
def vehicles_list(request):
    if request.method == 'GET':
        vehicles = Vehicle.objects.all()
        serializer = VehicleDetailSerializer(vehicles, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = VehicleSerializer(data=data)
        if serializer.is_valid():
            with transaction.atomic():
                vehicle = serializer.save()
                if 'scenarios' in data:
                    sync_vehicle_scenarios(vehicle, data['scenarios'])
                if 'recharge_speeds' in data:
                    sync_vehicle_recharge_speeds(vehicle, data['recharge_speeds'])
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET', 'PATCH', 'DELETE'])
def vehicle_detail(request, vehicle_pk):
    try:
        vehicle = Vehicle.objects.get(pk=vehicle_pk)
    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehicle not found'}, status=404)

    if request.method == 'GET':
        serializer = VehicleDetailSerializer(vehicle)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        serializer = VehicleSerializer(vehicle, data=data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                vehicle = serializer.save()
                if 'scenarios' in data:
                    sync_vehicle_scenarios(vehicle, data['scenarios'])
                if 'recharge_speeds' in data:
                    sync_vehicle_recharge_speeds(vehicle, data['recharge_speeds'])
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        vehicle.delete()
        return JsonResponse({'message': 'Vehicle deleted'}, status=204)
