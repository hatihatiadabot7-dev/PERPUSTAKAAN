"""
WSGI config for sipustaka project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys

# Mengarahkan ke folder utama kamu di PythonAnywhere
path = '/home/aisyarkaanabdurrahman/APLIKASI-PERPUSTAKAAN-DJANGO-SQL/sipustaka'
if path not in sys.path:
    sys.path.append(path)

# Mengarahkan ke nama folder project django kamu (sipustaka)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sipustaka.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()