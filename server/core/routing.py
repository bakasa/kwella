from django.urls import path

from trips.consumers import TripConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
from .middleware import TokenAuthMiddlewareStack

# websocket_urlpatterns = [
#     path(r'ws/trip/', TripConsumer.as_asgi()),
# ]


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddlewareStack(
        URLRouter(
            [path(r'ws/trip/', TripConsumer.as_asgi()),]
        )
    )

})
