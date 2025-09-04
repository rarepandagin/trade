"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""
# mysite/asgi.py
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import dashboard.routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(dashboard.routing.websocket_urlpatterns))
        ),
})



