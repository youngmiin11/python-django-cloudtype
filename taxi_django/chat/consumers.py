import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def websocket_receive(self, message):
        if 'text' in message:
            await self.receive(text_data=message['text'])
        elif 'bytes' in message:
            text_data = message['bytes'].decode('utf-8')
            await self.receive(text_data=text_data)
        else:
            print("Received non-text message:", message)

    async def receive(self, text_data):
        print("Received text data:", text_data)
        try:
            text_data_json = json.loads(text_data)
            user = text_data_json['user']
            message = text_data_json['message']

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'user': user,
                    'message': message,
                }
            )
        except json.JSONDecodeError:
            print("Failed to decode JSON message:", text_data)
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON'
            }))
        except TypeError:
            print("Received non-dictionary message:", text_data)
            await self.send(text_data=json.dumps({
                'error': 'Non-dictionary message'
            }))
        except KeyError:
            print("Message does not contain 'user' or 'message' key:", text_data_json)
            await self.send(text_data=json.dumps({
                'error': "Message does not contain 'user' or 'message' key"
            }))

    # Receive message from room group
    async def chat_message(self, event):
        user = event['user']
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'user': user,
            'message': message
        }))
