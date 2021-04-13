import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .serializers import DetailedTripSerializer, TripSerializer
from .models import Trip
from asgiref.sync import sync_to_async

# create trip helper function
class TripConsumer(AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def _create_trip(self, data):
        serializer = TripSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.create(serializer.validated_data)
    
    @database_sync_to_async
    def _get_trip_data(self, trip):
        return DetailedTripSerializer(trip).data
    
    @database_sync_to_async
    def _get_trip_ids(self, user):
        if user.type == 'DRIVER':
            trip_ids = user.trips_as_driver.exclude(status='COMPLETED').only('id').values_list('id', flat=True)
        elif user.type == 'RIDER':
            trip_ids = user.trips_as_rider.exclude(status='COMPLETED').only('id').values_list('id', flat=True)
        return map(str, trip_ids)

    async def connect(self):
        user = self.scope['user']
        if isinstance(user, AnonymousUser):
            await self.close()
        else:
            if user.type == "DRIVER":
                await self.channel_layer.group_add(
                    group='drivers',
                    channel=self.channel_name
                )
            
            # on Websocket connection
            # add user to all existing trip groups, they're associated with
            for trip_id in await self._get_trip_ids(user):
                await self.channel_layer.group_add(
                    group=trip_id,
                    channel=self.channel_name
                )

            await self.accept()
            
    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        if message_type == 'create.trip':
            await self.create_trip(content)

        elif message_type == 'echo.message':
            await self.echo_message(content)
    
    async def create_trip(self, message):
        # create trip into the db
        data = message.get('data')
        trip = await self._create_trip(data)
        trip_data = await self._get_trip_data(trip)

        # broadcast ride request to all drivers
        await self.channel_layer.group_send(
            group='drivers',
            message={
                'type': 'echo.message',
                'data': trip_data
            }
        )

        # add rider to trip group
        await self.channel_layer.group_add(
            group=f'{trip.id}',
            channel=self.channel_name
        )
        
        await self.send_json({
            'type': 'echo.message',
            'data': trip_data
        })

    async def echo_message(self, message):
        await self.send_json(message)

    async def disconnect(self, code):
        user = self.scope['user']

        if isinstance(user, AnonymousUser):
            await self.close()
        else:
            if user.type == 'DRIVER':
                await self.channel_layer.group_discard(
                    group='drivers',
                    channel=self.channel_name
                )
            
            # on Websocket connection
            # add user to all existing trip groups, they're associated with
            for trip_id in await self._get_trip_ids(user):
                await self.channel_layer.group_discard(
                    group=trip_id,
                    channel=self.channel_name
                )

            await super().disconnect(code)
 
