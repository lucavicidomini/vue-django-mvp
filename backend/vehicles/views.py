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
    VehicleScenarioSyncSerializer,
)

def sync_vehicle_scenarios(vehicle, data):
    serializer = VehicleScenarioSyncSerializer(data=data, many=True)
    if not serializer.is_valid():
        raise ValidationError({'scenarios': serializer.errors})

    existing = {scenario.pk: scenario for scenario in vehicle.vehiclescenario_set.all()}
    scenario_ids = [item['id'] for item in serializer.validated_data if item['id'] != 0]
    if len(scenario_ids) != len(set(scenario_ids)):
        raise ValidationError({'scenarios': 'Scenario IDs must not be repeated.'})
    if any(scenario_id not in existing for scenario_id in scenario_ids):
        raise ValidationError({'scenarios': 'Scenario IDs must belong to this vehicle.'})

    vehicle.vehiclescenario_set.exclude(pk__in=scenario_ids).delete()
    for scenario_data in serializer.validated_data:
        scenario_id = scenario_data.pop('id')
        if scenario_id == 0:
            serializer.child.create({**scenario_data, 'vehicle': vehicle})
        else:
            serializer.child.update(existing[scenario_id], scenario_data)

@api_view(['GET', 'POST'])
def vehicles_list(request):
    if request.method == 'GET':
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = VehicleSerializer(data=data)
        if serializer.is_valid():
            with transaction.atomic():
                vehicle = serializer.save()
                if 'scenarios' in data:
                    sync_vehicle_scenarios(vehicle, data['scenarios'])
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
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        vehicle.delete()
        return JsonResponse({'message': 'Vehicle deleted'}, status=204)

@api_view(['GET', 'POST'])
def vehicle_scenarios_list(request, vehicle_pk):
    if request.method == 'GET':
        scenarios = VehicleScenario.objects.filter(vehicle_id=vehicle_pk)
        serializer = VehicleScenarioSerializer(scenarios, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data['vehicle'] = vehicle_pk
        serializer = VehicleScenarioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET', 'PATCH', 'DELETE'])
def vehicle_scenarios_detail(request, vehicle_pk, scenario_pk):
    try:
        scenario = VehicleScenario.objects.get(pk=scenario_pk)
    except VehicleScenario.DoesNotExist:
        return JsonResponse({'error': 'Vehicle Scenario not found'}, status=404)

    if request.method == 'GET':
        serializer = VehicleScenarioSerializer(scenario)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        serializer = VehicleScenarioSerializer(scenario, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        scenario.delete()
        return JsonResponse({'message': 'Vehicle Scenario deleted'}, status=204)