"""
ASGI config for config project.

Он предоставляет возможность вызова ASGI в качестве переменной уровня модуля с именем `application`.
Для получения дополнительной информации об этом файле см.
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()