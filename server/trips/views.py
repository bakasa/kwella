from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from users.textchoices import UserTypes

from trips.models import TripStatus

from .models import Trip
from .serializers import TripSerializer, DetailedTripSerializer


class TripViewSet(viewsets.ReadOnlyModelViewSet): #Why readonly
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = DetailedTripSerializer
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if user.type == UserTypes.driver:
            return Trip.objects.filter(
                Q(status=TripStatus.requested) | Q(driver=user)
            )
        if user.type == UserTypes.rider:
            return Trip.objects.filter(rider=user)
        return super().get_queryset()
    
