# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]

#checkout/routing.py
'''
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/checkout/$', consumers.CheckoutConsumer),
]
'''
'''
# ecomsite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import checkout.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            checkout.routing.websocket_urlpatterns
        )
    ),
})
'''
