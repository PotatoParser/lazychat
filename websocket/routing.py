from django.urls import path
from channels.routing import URLRouter
from .consumers import WebSocket

# Sub level routing
websockets = URLRouter([
	path('', WebSocket)
])