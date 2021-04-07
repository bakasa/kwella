from django.shortcuts import render
from rest_framework import generics, permissions, viewsets

from .models import Trip
from .serializers import TripSerializer

class TripViewSet(viewsets.ReadOnlyModelViewSet): #Why readonly
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    lookup_field = 'id'