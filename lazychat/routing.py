from channels.routing import ProtocolTypeRouter
from websocket.routing import websockets

# High level routing
application = ProtocolTypeRouter({
	'websocket': websockets
})