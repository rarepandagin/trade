import codecs
import json
import compress_pickle

from channels.generic.websocket import AsyncWebsocketConsumer
from threading import Thread

ws_key = '26d25f4f-cd7d-4482-aae2-8a80781a33d4'

def decompress_pickle_object(obj):
    return compress_pickle.loads(codecs.decode(obj.encode(), "base64"), compression="gzip")


class websocker_consumer_dashboard(AsyncWebsocketConsumer):
    async def connect(self):

        _, protocol, _, user_id, _ = self.scope['path'].split('/')

        self.user_id = 1

        self.room_name = f"chat_{user_id}"
        self.room_group_name = self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(decompress_pickle_object(text_data))

        if 'key' not in text_data_json:
            return

        if text_data_json['key'] != ws_key:
            return

        message = text_data_json['message']
        topic = message['topic']

        if topic == 'new_project':

            # unless it is done, it is a not concern to db; but rather only to the JS
            if 'completed' in message:

                t = Thread(
                    target=ws_new_project.handle_new_projects,
                    args=(message,)
                )
                t.start()


        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'message_channel_dashboard',
                'message': message
            }
        )

    # Receive message from room group
    async def message_channel_dashboard(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

