from django.shortcuts import render
from django.http import JsonResponse
from django.db import transaction

from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from fuels.models import Fuel
from fuels.serializers import FuelSerializer


@api_view(['GET'])
def fuels_list(request):
    fuels = Fuel.objects.all()
    serializer = FuelSerializer(fuels, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['PATCH'])
def fuel_detail(request, fuel_pk):
    try:
        fuel = Fuel.objects.get(pk=fuel_pk)
    except Fuel.DoesNotExist:
        return JsonResponse({'error': 'Fuel not found'}, status=404)

    if request.method == 'PATCH':
        data = JSONParser().parse(request)
        serializer = FuelSerializer(fuel, data=data, partial=True)
        if serializer.is_valid():
            fuel = serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
