import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_views_routing_homework.settings')

application = get_wsgi_application()
