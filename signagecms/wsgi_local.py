"""
WSGI config for signagecms project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
activate_this = 'c:/users/jitendra/envs/gc_xamp/Scripts/activate_this.py'


# execfile(activate_this, dict(__file__=activate_this))

exec(open(activate_this).read(),dict(__file__=activate_this))

import sys
import site
import os

from django.core.wsgi import get_wsgi_application

# Add the site-packages of the chosen virtualenv to work with


site.addsitedir('c:/users/jitendra/envs/gc_xamp/Lib/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('C:/Users/Jitendra/python_projects/green_content')
sys.path.append('C:/Users/Jitendra/python_projects/green_content/signagecms')

os.environ['DJANGO_SETTINGS_MODULE'] = 'signagecms.settings'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "signagecms.settings")

application = get_wsgi_application()
