

import socket
hostname = socket.gethostname()
host_private_ip = socket.gethostbyname(hostname)
import time
import numpy as np


from dashboard.modules.logger import logger_class

import json
import uuid
import compress_pickle
import codecs
import json
import os
from datetime import datetime
from django.conf import settings
from django.core import serializers
from random_username.generate import generate_username

from dashboard.modules.notification.notification import NotificationClass


root_path = settings.BASE_DIR

dashboard_app_folder = os.path.join(root_path, 'dashboard')

modules_folder = os.path.join(dashboard_app_folder, 'modules')

modules_folder_path = os.path.join(dashboard_app_folder, 'modules')
dapp_folder_path = os.path.join(modules_folder_path, 'dapps')

uniswap_dapp_folder_path = os.path.join(dapp_folder_path, 'uniswap')
aave_dapp_folder_path = os.path.join(dapp_folder_path, 'aave')
arbi_dapp_folder_path = os.path.join(dapp_folder_path, 'arbi')

redirect_to_login = '/login/'
redirect_to_dashboard = '/dashboard/'
redirect_to_logout = '/logout/'








# LOGEGR
logger = logger_class.logger_model()






def exponential_moving_average(values, window_size, alpha=None):
    """
    Calculate the Exponential Moving Average (EMA) for a list of values.
    
    Parameters:
    values (list or array-like): The input data series.
    window_size (int): The number of periods to use for the EMA calculation.
    alpha (float, optional): The smoothing factor (0 < alpha < 1). If None, it is calculated as 2/(1+window_size).
    
    Returns:
    numpy.ndarray: An array of EMA values.
    """
    # Convert input to numpy array
    values = np.array(values)
    
    # Validate inputs
    if window_size <= 0:
        raise ValueError("window_size must be a positive integer.")
    if alpha is None:
        alpha = 2 / (1 + window_size)
    if not (0 < alpha < 1):
        raise ValueError("alpha must be between 0 and 1.")
    
    # Initialize EMA array
    ema = np.zeros_like(values)
    
    # First EMA value is the first value in the series
    ema[0] = values[0]
    
    # Calculate EMA for the rest of the values
    for i in range(1, len(values)):
        ema[i] = alpha * values[i] + (1 - alpha) * ema[i-1]
    
    return ema




def serialize_object(object):
    ret = json.loads(serializers.serialize('json', [object]))[0]['fields']
    ret['id'] = object.id
    return ret





def datetime_to_string(date_time_):
    return date_time_.strftime('%Y/%m/%d %H:%M:%S')


def string_to_datetime(date_time_string):
    return datetime.strptime(date_time_string, "%Y/%m/%d %H:%M:%S")


def compress_pickle_object(obj):
    return codecs.encode(compress_pickle.dumps(obj, "gzip"), "base64").decode()


def decompress_pickle_object(obj):
    return compress_pickle.loads(codecs.decode(obj.encode(), "base64"), compression="gzip")



def get_epoch_now():
    return int(time.time())


def get_new_uuid():
    return f"{uuid.uuid4()}".replace("-", '')

def get_admin_settings():
    from dashboard.models import AdminSettings
    return AdminSettings.objects.all()[0]

def get_new_random_name():
    return generate_username(1)[0]

def create_new_notification(title, message):
    notification = NotificationClass()
    notification.send(title=title, message= message)
                




def send_message_to_frontend_dashboard(topic, payload):
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync   


    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'room_group_name_dashboard',  # The group name
        {
        'type': 'message_channel_dashboard',
        'message': {
            "topic": topic,
            "payload": payload
            }
        }
    )
    


def send_message_to_frontend_depth(topic, payload):
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync   


    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'room_group_name_depth',  # The group name
        {
        'type': 'message_channel_depth',
        'message': {
            "topic": topic,
            "payload": payload
            }
        }
    )
    