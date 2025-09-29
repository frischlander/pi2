import os
import sys

# Adiciona o diretório raiz do projeto ao PythonPath
<<<<<<< HEAD
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

=======
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
>>>>>>> 7e403d9a0edb7fc3fc0b12150895b5d2b76b65ce

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conectacaa.settings")

application = get_wsgi_application()

