from django.urls import path

from .consumers import TripConsumer

websocket_urlpatterns = [
    path(r'ws/trip/', TripConsumer.as_asgi()),
]
