
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync  


async def send_message_to_frontend_async(payload):
    channel_layer = get_channel_layer()
    
    # Directly send message asynchronously
    await channel_layer.group_send(
            'room_group_name',  # The group name
            {
            'type': 'message_channel_dashboard',
            'message': {
                "topic": "update_positions_table",
                "payload": payload
                }
            }
    )