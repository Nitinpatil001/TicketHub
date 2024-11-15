"""
WSGI config for ticketing_tool project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

# Add your project directory to the sys.path
project_home = '/home/NitinPatil/Ticketing_Website'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set the DJANGO_SETTINGS_MODULE to your settings file
os.environ['DJANGO_SETTINGS_MODULE'] = 'Ticketing_Website.settings'

# Import the WSGI application from Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

