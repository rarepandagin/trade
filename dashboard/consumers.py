import codecs
import json
import compress_pickle
from channels.generic.websocket import AsyncWebsocketConsumer

ws_key = 'XiKd2uXZuT5vBU5mr2Qi'

def decompress_pickle_object(obj):
    return compress_pickle.loads(codecs.decode(obj.encode(), "base64"), compression="gzip")


class websocket_consumer_dashboard(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_name = "room_name_dashboard"
        self.room_group_name = "room_group_name_dashboard"

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

        if text_data_json.get('key', '') != ws_key:
            return

        message = text_data_json['message']

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


class websocket_consumer_depth(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_name = "room_name_depth"
        self.room_group_name = "room_group_name_depth"

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

        if text_data_json.get('key', '') != ws_key:
            return

        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'message_channel_depth',
                'message': message
            }
        )

    # Receive message from room group
    async def message_channel_depth(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

