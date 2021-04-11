import json

import pytest
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.urls import path
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
from rest_framework_simplejwt.tokens import AccessToken

# overwrite the application's settings to use InMemoryChannelLayer instead of
# the configured RedisChannelLayer
TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# test consumer
class TestConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        if isinstance(user, AnonymousUser):
            return await self.close()

        await self.channel_layer.group_add(
            group='test',
            channel=self.channel_name
        )

        return await super().connect()

    async def receive_json(self, content, **kwargs):
        message_type = content.get('type')
        if (message_type == 'echo.message'):
            await self.send_json({
                "type": message_type,
                "data": content.get("data")
            })
        return await super().receive_json(content, **kwargs)

    async def echo_message(self, message):
        await self.send_json({
            'type': message.get('type'),
            'data': message.get('data')
        })

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            group='test',
            channel=self.channel_name
        )
        return await super().disconnect(code)
# pytest warning about test collection
TestConsumer.__test__ = False

@database_sync_to_async
def create_user(phone_number, password):
    user = get_user_model().objects.create_user(
        phone_number=phone_number,
        password=password
    )

    access = AccessToken.for_user(user)

    return (user, access)

# instruct pytest to treat the tests as asyncio coroutines
@pytest.mark.asyncio  # mark sets metadata on each of the methods contained within
@pytest.mark.django_db(transaction=True) # add mark for accessing the database
class TestWebSocket:
    # settings is a fixture provided by pytest-django
    async def test_can_connect_to_server(self, settings):
        # configure test channel layer on settings
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user('0731245689', 'ilovethispassword')

        application = JWTAuthMiddlewareStack(
            URLRouter([
                path('ws/trip/', TestConsumer.as_asgi()),
            ])
        )
        
        communicator = WebsocketCommunicator(
            application=application,
            path=f'ws/trip/?token={access}'
        )

        connected, subprotocol = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_can_send_and_recieve_message(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user('0731245689', 'ilovethispassword')

        application = JWTAuthMiddlewareStack(
            URLRouter([
                path('ws/trip/', TestConsumer.as_asgi()),
            ])
        )

        communicator = WebsocketCommunicator(
            application=application,
            path=f'ws/trip/?token={access}'
        )

        connected, _ = await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'This is a test message',
        }

        await communicator.send_json_to(message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_can_send_and_recieve_broadcast_message(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        
        user, access = await create_user('0731245689', 'ilovethispassword')

        application = JWTAuthMiddlewareStack(
            URLRouter([
                path('ws/trip/', TestConsumer.as_asgi()),
            ])
        )

        communicator = WebsocketCommunicator(
            application=application,
            path=f'ws/trip/?token={access}'
        )

        connected, _ = await communicator.connect()
        message = {
            'type': 'echo.message',
            'data': 'This is a test message',
        }

        channel_layer = get_channel_layer()
        await channel_layer.group_send('test', message=message)
        response = await communicator.receive_json_from()
        assert response == message
        await communicator.disconnect()

    async def test_cannot_connect_to_socket_without_valid_token(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS

        user, access = await create_user('0731245689', 'ilovethispassword')

        application = JWTAuthMiddlewareStack(
            URLRouter([
                path('ws/trip/', TestConsumer.as_asgi()),
            ])
        )

        communicator = WebsocketCommunicator(
            application=application,
            path=f'ws/trip/?token='
        )

        connected, _ = await communicator.connect()
        assert connected is False
        await communicator.disconnect()
