"""
Analytics Module for Food Recommendation System
Provides insights into user behavior and system performance
"""

from django.db.models import Count, Avg, Sum, Q
from django.contrib.auth.models import User
from collections import Counter
from .models import (
    OrderPlaced, ChefProduct, Product, UserInteraction,
    RecommendationLog, Customer
)


class RecommendationAnalytics:
    """
    Analyze recommendation system performance.
    Useful for interviews to show you understand ML evaluation.
    """

    @staticmethod
    def get_recommendation_stats():
        """
        Get overall recommendation system statistics.

        Returns:
            dict: Key metrics about recommendations
        """
        total_recommendations = RecommendationLog.objects.count()
        total_clicks = RecommendationLog.objects.filter(clicked=True).count()

        click_through_rate = 0
        if total_recommendations > 0:
            click_through_rate = (total_clicks / total_recommendations) * 100

        # Breakdown by recommendation type
        type_breakdown = RecommendationLog.objects.values('recommendation_type').annotate(
            count=Count('id')
        )

        return {
            'total_recommendations_shown': total_recommendations,
            'total_clicks': total_clicks,
            'click_through_rate': round(click_through_rate, 2),
            'recommendation_type_breakdown': list(type_breakdown)
        }

    @staticmethod
    def get_most_recommended_products(limit=10):
        """
        Get products that are most frequently recommended.

        Returns:
            list: Product IDs with recommendation counts
        """
        all_recommendations = RecommendationLog.objects.all()

        product_counter = Counter()

        for rec_log in all_recommendations:
            for product_id in rec_log.recommended_products:
                product_counter[product_id] += 1

        most_common = product_counter.most_common(limit)

        results = []
        for product_id, count in most_common:
            try:
                chef_product = ChefProduct.objects.get(id=product_id)
                results.append({
                    'product_id': product_id,
                    'product_name': chef_product.product_name,
                    'recommendation_count': count
                })
            except ChefProduct.DoesNotExist:
                continue

        return results


class UserAnalytics:
    """
    Analyze user behavior patterns.
    """

    @staticmethod
    def get_user_stats():
        """
        Get overall user statistics.

        Returns:
            dict: User metrics
        """
        total_users = User.objects.count()
        users_with_orders = User.objects.filter(orderplaced__isnull=False).distinct().count()
        users_with_profile = Customer.objects.count()

        avg_orders_per_user = 0
        if users_with_orders > 0:
            total_orders = OrderPlaced.objects.count()
            avg_orders_per_user = total_orders / users_with_orders

        return {
            'total_users': total_users,
            'users_with_orders': users_with_orders,
            'users_with_profile': users_with_profile,
            'conversion_rate': round((users_with_orders / total_users * 100), 2) if total_users > 0 else 0,
            'avg_orders_per_user': round(avg_orders_per_user, 2)
        }

    @staticmethod
    def get_user_preferences_distribution():
        """
        Get distribution of user preferences.

        Returns:
            dict: Preference distributions
        """
        category_dist = Customer.objects.values('category_preference').annotate(
            count=Count('id')
        )

        cuisine_dist = Customer.objects.values('cuisine_preference').annotate(
            count=Count('id')
        )

        return {
            'category_distribution': list(category_dist),
            'cuisine_distribution': list(cuisine_dist)
        }


class ProductAnalytics:
    """
    Analyze product performance.
    """

    @staticmethod
    def get_top_selling_products(limit=10):
        """
        Get best-selling products.

        Returns:
            QuerySet: Top selling ChefProduct objects
        """
        return ChefProduct.objects.annotate(
            total_sold=Count('orderplaced')
        ).filter(total_sold__gt=0).order_by('-total_sold')[:limit]

    @staticmethod
    def get_product_stats():
        """
        Get overall product statistics.

        Returns:
            dict: Product metrics
        """
        total_products = Product.objects.count()
        total_chef_variants = ChefProduct.objects.count()

        avg_price = ChefProduct.objects.aggregate(Avg('discounted_price'))['discounted_price__avg']
        avg_rating = ChefProduct.objects.aggregate(Avg('ratings'))['ratings__avg']

        category_breakdown = ChefProduct.objects.values('category').annotate(
            count=Count('id')
        )

        cuisine_breakdown = Product.objects.values('cuisine').annotate(
            count=Count('id')
        )

        meal_type_breakdown = ChefProduct.objects.values('meal_type').annotate(
            count=Count('id')
        )

        return {
            'total_base_products': total_products,
            'total_chef_variants': total_chef_variants,
            'avg_variants_per_product': round(total_chef_variants / total_products, 2) if total_products > 0 else 0,
            'avg_price': round(avg_price, 2) if avg_price else 0,
            'avg_rating': round(avg_rating, 2) if avg_rating else 0,
            'category_breakdown': list(category_breakdown),
            'cuisine_breakdown': list(cuisine_breakdown),
            'meal_type_breakdown': list(meal_type_breakdown)
        }

    @staticmethod
    def get_most_viewed_products(limit=10):
        """
        Get most viewed products based on interactions.

        Returns:
            list: Products with view counts
        """
        product_views = UserInteraction.objects.filter(
            interaction_type='view'
        ).values('chef_product').annotate(
            view_count=Count('id')
        ).order_by('-view_count')[:limit]

        results = []
        for item in product_views:
            if item['chef_product']:
                try:
                    chef_product = ChefProduct.objects.get(id=item['chef_product'])
                    results.append({
                        'product': chef_product,
                        'view_count': item['view_count']
                    })
                except ChefProduct.DoesNotExist:
                    continue

        return results


class OrderAnalytics:
    """
    Analyze order patterns.
    """

    @staticmethod
    def get_order_stats():
        """
        Get overall order statistics.

        Returns:
            dict: Order metrics
        """
        total_orders = OrderPlaced.objects.count()

        if total_orders == 0:
            return {
                'total_orders': 0,
                'total_revenue': 0,
                'avg_order_value': 0
            }

        total_revenue = sum(order.total_price for order in OrderPlaced.objects.all())
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

        # Orders by meal type
        meal_type_breakdown = OrderPlaced.objects.values('product__meal_type').annotate(
            count=Count('id')
        )

        # Orders by category
        category_breakdown = OrderPlaced.objects.values('product__category').annotate(
            count=Count('id')
        )

        return {
            'total_orders': total_orders,
            'total_revenue': round(total_revenue, 2),
            'avg_order_value': round(avg_order_value, 2),
            'meal_type_breakdown': list(meal_type_breakdown),
            'category_breakdown': list(category_breakdown)
        }

    @staticmethod
    def get_repeat_purchase_rate():
        """
        Calculate how many users make repeat purchases.

        Returns:
            dict: Repeat purchase metrics
        """
        users_with_orders = User.objects.filter(orderplaced__isnull=False).distinct()
        total_users_ordered = users_with_orders.count()

        if total_users_ordered == 0:
            return {
                'repeat_customers': 0,
                'repeat_rate': 0
            }

        repeat_customers = 0
        for user in users_with_orders:
            order_count = OrderPlaced.objects.filter(user=user).count()
            if order_count > 1:
                repeat_customers += 1

        repeat_rate = (repeat_customers / total_users_ordered) * 100

        return {
            'total_customers': total_users_ordered,
            'repeat_customers': repeat_customers,
            'repeat_rate': round(repeat_rate, 2)
        }


def get_dashboard_metrics():
    """
    Get all key metrics for a dashboard view.
    Useful for interviews to show business understanding.

    Returns:
        dict: Comprehensive system metrics
    """
    return {
        'user_metrics': UserAnalytics.get_user_stats(),
        'product_metrics': ProductAnalytics.get_product_stats(),
        'order_metrics': OrderAnalytics.get_order_stats(),
        'recommendation_metrics': RecommendationAnalytics.get_recommendation_stats(),
        'top_products': ProductAnalytics.get_top_selling_products(limit=5),
        'most_viewed': ProductAnalytics.get_most_viewed_products(limit=5),
        'repeat_purchase': OrderAnalytics.get_repeat_purchase_rate()
    }
