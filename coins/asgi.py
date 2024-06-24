import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import showing.routing  # Import your routing configuration

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coins.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            showing.routing.websocket_urlpatterns
        )
    ),
})
