from django.urls import path
from .views import pharmacies_list

urlpatterns = [
    path('pharmacies/', pharmacies_list, name='pharmacies_list'),
]