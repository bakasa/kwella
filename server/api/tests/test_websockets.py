import pytest
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from core.asgi import application
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
import json

# overwrite the application's settings to use InMemoryChannelLayer instead of
# the configured RedisChannelLayer
TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

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

        communicator = WebsocketCommunicator(
            application=application,
            path=f'ws/trip/?token='
        )

        connected, _ = await communicator.connect()
        assert connected is False
        await communicator.disconnect()
