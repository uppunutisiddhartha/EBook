# routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/collaboration/<uuid:session_id>/', consumers.CollaborationConsumer.as_asgi()),
]
