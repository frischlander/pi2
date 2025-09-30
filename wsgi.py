import os

# Define as configurações do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

