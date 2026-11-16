from django.urls import path
from .views import fuels_list, fuel_detail

urlpatterns = [
    path("", fuels_list),
    path("<int:fuel_pk>/", fuel_detail),
]