import os
import sys

# Adiciona o diretório raiz do projeto ao PythonPath
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conectacaa.settings")

application = get_wsgi_application()

