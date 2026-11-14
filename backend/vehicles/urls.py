from django.urls import path
from .views import vehicles_list, vehicle_detail, vehicle_scenarios_list, vehicle_scenarios_detail

urlpatterns = [
    path("", vehicles_list),
    path("<int:vehicle_pk>/", vehicle_detail),
    path("<int:vehicle_pk>/scenarios/", vehicle_scenarios_list),
    path("<int:vehicle_pk>/scenarios/<int:scenario_pk>/", vehicle_scenarios_detail),
]