


import boto3_class

boto3_handler = boto3_class.Boto3Class(bucket_name='unrealizer-statics')



boto3_handler.upload_file_to_s3('/home/user/Desktop/trade/dashboard/static/js/js_routines_dashboard.js',     'js_routines_dashboard.js')
boto3_handler.upload_file_to_s3('/home/user/Desktop/trade/dashboard/static/js/js_routines_depth.js',         'js_routines_depth.js')
boto3_handler.upload_file_to_s3('/home/user/Desktop/trade/dashboard/static/js/ajax_handler.js',              'ajax_handler.js')
boto3_handler.upload_file_to_s3('/home/user/Desktop/trade/dashboard/static/js/pairs.js',                     'pairs.js')
boto3_handler.upload_file_to_s3('/home/user/Desktop/trade/dashboard/static/js/bot.js',                       'bot.js')
boto3_handler.upload_file_to_s3('/home/user/Desktop/trade/dashboard/static/js/websocket_manager.js',         'websocket_manager.js')
boto3_handler.upload_file_to_s3('/home/user/Desktop/trade/dashboard/static/css/style.css',                   'style.css')