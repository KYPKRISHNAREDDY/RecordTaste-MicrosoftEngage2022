"""
ASGI config for FoodRecommendationSystem project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FoodRecommendationSystem.settings')

application = get_asgi_application()
