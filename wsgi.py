import os
import sys

<<<<<<< HEAD
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
=======
<<<<<<< HEAD
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
=======
<<<<<<< HEAD
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

=======
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
>>>>>>> 7e403d9a0edb7fc3fc0b12150895b5d2b76b65ce
>>>>>>> 03aaf15e87c501fbcfade3d3d0dc3cdf093cb61c
>>>>>>> 50c95bb53b28d10e607a7abcc0f289f657cb1e2d

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conectacaa.settings")

application = get_wsgi_application()

