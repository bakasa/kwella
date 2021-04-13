import json

import pytest
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from core.routing import application
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

# overwrite the application's settings to use InMemoryChannelLayer instead of
# the configured RedisChannelLayer
TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

@database_sync_to_async
def create_user(phone_number, password, user_type='RIDER'):
    user = get_user_model().objects.create_user(
        phone_number=phone_number,
        password=password,
        type=user_type,
        is_active=True
    )

    access = AccessToken.for_user(user)

    return (user, access)

# instruct pytest to treat the tests as asyncio coroutines
@pytest.mark.asyncio  # mark sets metadata on each of the methods contained within
@pytest.mark.django_db(transaction=True) # add mark for accessing the database
class TestWebSocket:
    # # settings is a fixture provided by pytest-django
    # async def test_can_connect_to_server(self, settings):
    #     # configure test channel layer on settings
    #     settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    #     user, access = await create_user('0731245689', 'ilovethispassword')
        
    #     communicator = WebsocketCommunicator(
    #         application=application,
    #         path=f'ws/trip/?token={access}'
    #     )

    #     connected, subprotocol = await communicator.connect()
    #     assert connected is True
    #     await communicator.disconnect()

    # async def test_can_send_and_recieve_message(self, settings):
    #     settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
    #     user, access = await create_user('0731245689', 'ilovethispassword')

    #     communicator = WebsocketCommunicator(
    #         application=application,
    #         path=f'ws/trip/?token={access}'
    #     )

    #     connected, _ = await communicator.connect()
    #     message = {
    #         'type': 'echo.message',
    #         'data': 'This is a test message',
    #     }

    #     await communicator.send_json_to(message)
    #     response = await communicator.receive_json_from()
    #     assert response == message
    #     await communicator.disconnect()

    # async def test_driver_can_join_driver_pool(self, settings):
    #     settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        
    #     user, access = await create_user('0731245689', 'ilovethispassword', 'DRIVER')

    #     communicator = WebsocketCommunicator(
    #         application=application,
    #         path=f'ws/trip/?token={access}'
    #     )

    #     connected, _ = await communicator.connect()
    #     message = {
    #         'type': 'echo.message',
    #         'data': 'This is a test message',
    #     }

    #     channel_layer = get_channel_layer()
    #     await channel_layer.group_send('drivers', message=message)
    #     response = await communicator.receive_json_from()
    #     assert response == message
    #     await communicator.disconnect()

    # async def test_cannot_connect_to_socket_without_valid_token(self, settings):
    #     settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS

    #     user, access = await create_user('0731245689', 'ilovethispassword')

    #     communicator = WebsocketCommunicator(
    #         application=application,
    #         path=f'ws/trip/?token='
    #     )

    #     connected, _ = await communicator.connect()
    #     assert connected is False
    #     await communicator.disconnect()


    async def test_can_create_trip(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        user, access = await create_user('0731245689', 'ilovethispassword')
        communicator =  WebsocketCommunicator(application=application, path=f'ws/trip/?token={access}')

        trip_data = {
            'type': 'create.trip',
            'data': {
                'pickup': '123 Street Home Address',
                'dropoff': '456 Street Destination',
                'rider': user.id
            }
        }

        connected, subprotocol = await communicator.connect()
        await communicator.send_json_to(data=trip_data)

        response = await communicator.receive_json_from()
        # import pdb; pdb.set_trace()

        assert response.get('data')['id'] is not None
        assert response.get('data')['driver'] is None
        assert response.get('data')['status'] == 'REQUESTED'
        assert response.get('data')['pickup'] == trip_data.get('data')['pickup']
        assert response.get('data')['dropoff'] == trip_data.get('data')['dropoff']
        assert response.get('data')['rider']['id'] == user.id

        await communicator.disconnect()


