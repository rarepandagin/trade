import codecs
import json
import compress_pickle
from threading import Thread
from channels.generic.websocket import AsyncWebsocketConsumer
# from dashboard.ws_routines.ws_pulse_handler import handle_ws_pulse

ws_key = 'XiKd2uXZuT5vBU5mr2Qi'

def decompress_pickle_object(obj):
    return compress_pickle.loads(codecs.decode(obj.encode(), "base64"), compression="gzip")

class CustomThread(Thread):
    def __init__(self, target, args=()):
        super().__init__(target=target, args=args)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        super().join()
        return self._return

class websocker_consumer_dashboard(AsyncWebsocketConsumer):

    async def connect(self):

        _, _, _, _, _ = self.scope['path'].split('/')

        self.room_name = f"chat_1"
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
        # self.still_processing = True

        text_data_json = json.loads(decompress_pickle_object(text_data))

        if text_data_json.get('key', '') != ws_key:
            return

        message = text_data_json['message']
        topic = message['topic']


        # if topic == 'pulse':


        #     thread = CustomThread(target=handle_ws_pulse, args=(message,))
        #     thread.start()
        #     message_to_forward = thread.join()

        #     if message_to_forward is not None:

                # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'message_channel_dashboard',
                'message': message
            }
        )
                # self.still_processing = True

        # self.still_processing = False


    # Receive message from room group
    async def message_channel_dashboard(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

