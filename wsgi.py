import os
import sys

# Adiciona o diretório raiz do projeto ao PythonPath
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conectacaa.settings")

application = get_wsgi_application()

