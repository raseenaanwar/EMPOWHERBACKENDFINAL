
# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmpowherProject.settings')

# application = get_asgi_application()
# EmpowherProject/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.sessions import SessionMiddlewareStack
import chatapp.routing  # Import your chat routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmpowherProject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handles HTTP requests

    "websocket": AllowedHostsOriginValidator(
        SessionMiddlewareStack(
            AuthMiddlewareStack(
                URLRouter(
                    chatapp.routing.websocket_urlpatterns  # WebSocket routes
                )
            )
        )
    ),
})
