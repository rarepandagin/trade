PRODUCTION = False



"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv

from django.core.wsgi import get_wsgi_application



# Load environment variables from .env file
# Use the path relative to the wsgi.py file
if PRODUCTION:
    env_filepath = "/home/sammy/.env"
else:
    env_filepath = "/home/user/Desktop/.env"

load_dotenv(env_filepath)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()
