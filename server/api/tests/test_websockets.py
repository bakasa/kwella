import pytest
from channels.testing import WebsocketCommunicator
from core.asgi import application
from channels.layers import get_channel_layer


# overwrite the application's settings to use InMemoryChannelLayer instead of 
# the configured RedisChannelLayer
TEST_CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# instruct pytest to treat the tests as asyncio coroutines
@pytest.mark.asyncio #mark sets metadata on each of the methods contained within
class TestWebSocket:
    async def test_can_connect_to_server(self, settings): # settings is a fixture provided by pytest-django
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS # configure test channel layer on settings 
        communicator = WebsocketCommunicator(
            application=application,
            path='/trip/'
        )

        connected, _ = await communicator.connect()
        assert connected is True
        await communicator.disconnect()

    async def test_can_send_and_recieve_message(self, settings):
        settings.CHANNEL_LAYERS = TEST_CHANNEL_LAYERS
        communicator = WebsocketCommunicator(
            application=application,
            path='/trip/'
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
            communicator = WebsocketCommunicator(
                application=application,
                path='/trip/'
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

