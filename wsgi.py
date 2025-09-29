import os
import sys

# Adiciona a raiz do projeto ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Define as configurações do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conectaa.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


