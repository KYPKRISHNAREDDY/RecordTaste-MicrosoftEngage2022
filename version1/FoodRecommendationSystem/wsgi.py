"""
WSGI config for FoodRecommendationSystem project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FoodRecommendationSystem.settings')

application = get_wsgi_application()
