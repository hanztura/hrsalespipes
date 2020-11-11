"""
WSGI config for hrsalespipes project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys
import dotenv

from django.core.wsgi import get_wsgi_application

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv.read_dotenv(os.path.join(project_path, '.env'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

sys.path.append(os.path.join(project_path, 'hrsalespipes'))

application = get_wsgi_application()
