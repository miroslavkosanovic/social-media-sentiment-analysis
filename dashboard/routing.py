from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from sentiment_dashboard import consumers
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/dashboard/", consumers.DashboardConsumer.as_asgi()),
    ]),
})
