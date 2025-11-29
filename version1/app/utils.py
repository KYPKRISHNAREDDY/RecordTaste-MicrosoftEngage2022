"""
Utility functions for the Food Recommendation System
"""

from .models import UserInteraction, Product, ChefProduct


def log_user_interaction(user, product, interaction_type, chef_product=None, session_id=None):
    """
    Log user interactions for ML recommendation improvements.

    Args:
        user: Django User object (can be None for anonymous)
        product: Product object
        interaction_type: 'view', 'click', 'add_to_cart', 'purchase'
        chef_product: ChefProduct object (optional)
        session_id: Session ID for anonymous users (optional)

    Returns:
        UserInteraction object
    """
    interaction = UserInteraction.objects.create(
        user=user,
        product=product,
        chef_product=chef_product,
        interaction_type=interaction_type,
        session_id=session_id or ''
    )

    # Update product popularity
    if interaction_type in ['purchase', 'add_to_cart']:
        product.update_popularity()

    return interaction


def get_user_preference_summary(user):
    """
    Analyze user's preferences based on order history and interactions.

    Returns:
        dict: Summary of user preferences
    """
    from .models import OrderPlaced, Customer
    from collections import Counter

    summary = {
        'favorite_cuisine': None,
        'favorite_category': None,
        'favorite_meal_type': None,
        'avg_price_range': 0,
        'total_orders': 0,
    }

    orders = OrderPlaced.objects.filter(user=user)
    summary['total_orders'] = orders.count()

    if orders.exists():
        # Favorite cuisine
        cuisines = [order.product.titleid.cuisine for order in orders]
        cuisine_counter = Counter(cuisines)
        summary['favorite_cuisine'] = cuisine_counter.most_common(1)[0][0] if cuisine_counter else None

        # Favorite category (Veg/Non-veg)
        categories = [order.product.category for order in orders]
        category_counter = Counter(categories)
        summary['favorite_category'] = category_counter.most_common(1)[0][0] if category_counter else None

        # Favorite meal type
        meal_types = [order.product.meal_type for order in orders]
        meal_type_counter = Counter(meal_types)
        summary['favorite_meal_type'] = meal_type_counter.most_common(1)[0][0] if meal_type_counter else None

        # Average price range
        total_price = sum(order.product.discounted_price for order in orders)
        summary['avg_price_range'] = total_price / orders.count()

    return summary


def calculate_recommendation_accuracy(user, days=30):
    """
    Calculate how accurate our recommendations are for a user.

    Checks if recommended items were actually clicked/purchased.

    Args:
        user: Django User object
        days: Number of days to look back

    Returns:
        float: Accuracy percentage
    """
    from datetime import timedelta
    from django.utils import timezone
    from .models import RecommendationLog, UserInteraction

    cutoff_date = timezone.now() - timedelta(days=days)

    # Get recent recommendations
    recent_recs = RecommendationLog.objects.filter(
        user=user,
        shown_at__gte=cutoff_date
    )

    if not recent_recs.exists():
        return 0.0

    total_recommendations = 0
    successful_recommendations = 0

    for rec_log in recent_recs:
        recommended_ids = rec_log.recommended_products
        total_recommendations += len(recommended_ids)

        # Check if any recommended items were interacted with
        interactions = UserInteraction.objects.filter(
            user=user,
            chef_product_id__in=recommended_ids,
            timestamp__gte=rec_log.shown_at,
            interaction_type__in=['click', 'add_to_cart', 'purchase']
        )

        successful_recommendations += interactions.count()

    if total_recommendations == 0:
        return 0.0

    accuracy = (successful_recommendations / total_recommendations) * 100
    return round(accuracy, 2)


def get_popular_items_by_category(category=None, limit=10):
    """
    Get popular items, optionally filtered by category.

    Args:
        category: 'Vegetarian' or 'NonVegetarian' (optional)
        limit: Number of items to return

    Returns:
        QuerySet of ChefProduct objects
    """
    from django.db.models import Count

    queryset = ChefProduct.objects.annotate(
        order_count=Count('orderplaced')
    )

    if category:
        queryset = queryset.filter(category=category)

    return queryset.order_by('-order_count', '-ratings')[:limit]


def get_trending_items(days=7, limit=10):
    """
    Get trending items based on recent orders and views.

    Args:
        days: Number of days to consider for "trending"
        limit: Number of items to return

    Returns:
        QuerySet of ChefProduct objects
    """
    from datetime import timedelta
    from django.utils import timezone
    from django.db.models import Count, Q

    cutoff_date = timezone.now() - timedelta(days=days)

    # Items with recent orders
    trending = ChefProduct.objects.filter(
        Q(orderplaced__ordered_date__gte=cutoff_date) |
        Q(userinteraction__timestamp__gte=cutoff_date)
    ).annotate(
        recent_activity=Count('orderplaced') + Count('userinteraction')
    ).order_by('-recent_activity', '-ratings')[:limit]

    return trending


def get_complementary_items(chef_product, limit=6):
    """
    Get items that complement the given product.
    For example, if someone orders a main course, suggest beverages or desserts.

    Args:
        chef_product: ChefProduct object
        limit: Number of items to return

    Returns:
        QuerySet of ChefProduct objects
    """
    # Simple logic: if it's a main meal, suggest snacks/beverages
    # If it's a snack, suggest main meals

    if chef_product.meal_type in ['BreakFast', 'Lunch', 'Dinner']:
        complementary = ChefProduct.objects.filter(
            meal_type='Snacks'
        ).exclude(id=chef_product.id).order_by('-ratings')[:limit]
    else:
        complementary = ChefProduct.objects.filter(
            meal_type__in=['BreakFast', 'Lunch', 'Dinner']
        ).exclude(id=chef_product.id).order_by('-ratings')[:limit]

    return complementary
