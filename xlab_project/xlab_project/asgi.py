"""
ASGI config for xlab_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from xlab_chat_gpt import middlewares, consumers, routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xlab_project.settings')

asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": asgi_app,
    "websocket": AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)),
})
