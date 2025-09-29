import os
from django.core.wsgi import get_wsgi_application

# Ajuste para o nome correto do módulo de settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conectaa.settings")

application = get_wsgi_application()
