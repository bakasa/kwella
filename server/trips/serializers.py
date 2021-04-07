from rest_framework.serializers import ModelSerializer
from .models import Trip

class TripSerializer(ModelSerializer):
    class Meta:
        model = Trip
        fields = ('__all__')
        read_only_fields = ('id', 'created', 'updated', ) # ensure only the server can create/update these fields
    