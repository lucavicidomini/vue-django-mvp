from django.urls import path
from .views import vehicles_list, vehicle_detail

urlpatterns = [
    path("", vehicles_list),
    path("<int:vehicle_pk>/", vehicle_detail),
]