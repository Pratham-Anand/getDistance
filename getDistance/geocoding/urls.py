from django.urls import path
from . import views

urlpatterns = [
    path('distance/', views.DistanceCalculatorView.as_view(), name='geocode_city'),
]
