"""
WSGI config for pressfeed project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from pressfeed.tasks import start_scheduler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pressfeed.settings')

start_scheduler()

application = get_wsgi_application()
