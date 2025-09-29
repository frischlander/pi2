import os
from conectaa.wsgi import application


# Ajuste para o nome correto do módulo de settings do seu projeto Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pi2univesp.settings")

application = get_wsgi_application()
