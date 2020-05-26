import os, django
from django.core.handlers.wsgi import WSGIHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MOOSE_web.settings')
django.setup()
application = WSGIHandler()