

import socket
hostname = socket.gethostname()
host_private_ip = socket.gethostbyname(hostname)
import time


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
uniswap_module = os.path.join(modules_folder_path, 'uniswap')
abi_folder_path = os.path.join(uniswap_module, 'abis')


redirect_to_login = '/login/'
redirect_to_dashboard = '/dashboard/'
redirect_to_logout = '/logout/'








# LOGEGR
logger = logger_class.logger_model()










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
                


def create_fiat_to_token_transaction(fiat_to_token_amount, coin):
    from dashboard.models import models_transaction
    
    transaction = models_transaction.Transaction(
        coin=coin,
        transaction_type=models_transaction.fiat_to_token,
        fiat_amount_spent=fiat_to_token_amount,
    )

    transaction.save()
    
    transaction.actualize()

    transaction.save()

    return transaction


def create_token_to_fiat_transaction(token_to_fiat_amount, coin):
    from dashboard.models import models_transaction
    
    transaction = models_transaction.Transaction(
        coin=coin,
        transaction_type=models_transaction.token_to_fiat,
        token_amount_spent=token_to_fiat_amount,
    )

    transaction.save()
    
    transaction.actualize()

    transaction.save()

    return transaction
