from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculate_times, name='calculate_times'),
]