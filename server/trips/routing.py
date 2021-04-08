from django.urls import path

from .consumers import TripConsumer

websocket_urlpatterns = [
    path(r'trip/', TripConsumer.as_asgi()),
]
