from django.urls import path
from .consumers import VideoStreamConsumer

ws_urlpatterns = [
	path('ws/connect/', VideoStreamConsumer.as_asgi())
]