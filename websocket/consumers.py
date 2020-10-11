import random
import time

# Use AsyncJsonWebsocketConsumer instead of AsyncWebsocketConsumer for json encoding
from channels.generic.websocket import AsyncJsonWebsocketConsumer

# Creates the random name from a set of characters
randname = lambda l, scheme: ''.join(random.choices(scheme, k=l))

class WebSocket(AsyncJsonWebsocketConsumer):
	async def connect(self):

		# Accept the connection
		await self.accept()

		self.scope['username'] = randname(6, '56789ABCDEF') # Keep things in "scope"

		# Add the current connection to the group
		await self.channel_layer.group_add(
			'main',
			self.channel_name
		)
		
		# Send the generated username
		await self.send_json({
			'type': 'username',
			'username': self.scope['username'],
			'time': int(round(time.time() * 1000))
		})

	async def receive_json(self, content):

		# Only do things when the type is message
		if content['type'] == 'message':

			# Send data to the group
			await self.channel_layer.group_send(
				'main',
				{
					'type': 'message', # This references the event listener function
					'username': self.scope['username'],
					'message': content['message'],
					'time': int(round(time.time() * 1000)),
				}
			)

	async def message(self, event):

		# Sends the actual data to everyone
		await self.send_json({
			'type': 'message',
			'message': event['message'],
			'username': event['username'],
			'time': event['time'],
		})

	async def disconnect(self, close_code):

		# Disconnect the connection from the group
		await self.channel_layer.group_discard(
			'main',
			self.channel_name
		)