"""
ML-Based Recommendation Engine
Microsoft Engage 2022 - Food Recommendation System

This module implements a hybrid recommendation system combining:
1. Collaborative Filtering (User-based)
2. Content-Based Filtering (Item similarity)
3. Popularity-Based recommendations
4. Profile-Based recommendations

The system handles cold-start problems and provides explainable recommendations.
"""

from django.db.models import Count, Q, Avg
from collections import defaultdict, Counter
import math
from .models import (
    Product, ChefProduct, OrderPlaced, Customer,
    UserInteraction, RecommendationLog
)


class CollaborativeFiltering:
    """
    User-based Collaborative Filtering

    Finds similar users based on order history and recommends
    items that similar users have purchased.

    Similarity Metric: Jaccard Similarity
    Formula: |A ∩ B| / |A ∪ B|
    """

    def __init__(self, user):
        self.user = user
        self.user_orders = set(
            OrderPlaced.objects.filter(user=user)
            .values_list('product__titleid_id', flat=True)
        )

    def calculate_user_similarity(self, other_user):
        """
        Calculate Jaccard similarity between two users based on purchase history.

        Returns: float between 0 and 1 (higher = more similar)
        """
        if self.user.id == other_user.id:
            return 0

        other_orders = set(
            OrderPlaced.objects.filter(user=other_user)
            .values_list('product__titleid_id', flat=True)
        )

        if not self.user_orders or not other_orders:
            return 0

        intersection = self.user_orders.intersection(other_orders)
        union = self.user_orders.union(other_orders)

        if not union:
            return 0

        return len(intersection) / len(union)

    def find_similar_users(self, top_n=5):
        """
        Find top N similar users based on Jaccard similarity.

        Returns: List of (user, similarity_score) tuples
        """
        from django.contrib.auth.models import User

        all_users = User.objects.exclude(id=self.user.id)
        similarities = []

        for other_user in all_users:
            similarity = self.calculate_user_similarity(other_user)
            if similarity > 0:
                similarities.append((other_user, similarity))

        # Sort by similarity score (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_n]

    def get_recommendations(self, top_n=10):
        """
        Get product recommendations based on similar users' purchases.

        Returns: QuerySet of recommended ChefProduct objects
        """
        similar_users = self.find_similar_users(top_n=5)

        if not similar_users:
            return ChefProduct.objects.none()

        # Weighted recommendation scoring
        product_scores = defaultdict(float)

        for similar_user, similarity in similar_users:
            # Get products ordered by similar user
            similar_user_products = OrderPlaced.objects.filter(
                user=similar_user
            ).values_list('product_id', flat=True)

            for product_id in similar_user_products:
                # Don't recommend already purchased items
                if product_id not in self.user_orders:
                    product_scores[product_id] += similarity

        # Sort by score and get top N
        sorted_products = sorted(
            product_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]

        product_ids = [pid for pid, _ in sorted_products]

        return ChefProduct.objects.filter(id__in=product_ids)


class ContentBasedFiltering:
    """
    Content-Based Filtering using item attributes.

    Recommends items similar to those the user has interacted with
    based on cuisine, category, meal type, and price range.

    Similarity Metric: Weighted Feature Matching
    """

    def __init__(self, user=None):
        self.user = user

    def calculate_item_similarity(self, item1, item2):
        """
        Calculate similarity between two ChefProduct items.

        Features considered:
        - Cuisine (weight: 0.3)
        - Category (Veg/Non-veg) (weight: 0.25)
        - Meal Type (weight: 0.2)
        - Price Range (weight: 0.15)
        - Ratings (weight: 0.1)

        Returns: float between 0 and 1
        """
        score = 0.0

        # Cuisine match
        if item1.titleid.cuisine == item2.titleid.cuisine:
            score += 0.3

        # Category match (Veg/Non-veg)
        if item1.category == item2.category:
            score += 0.25

        # Meal type match
        if item1.meal_type == item2.meal_type:
            score += 0.2

        # Price similarity (within 20% range)
        price_diff = abs(item1.discounted_price - item2.discounted_price)
        avg_price = (item1.discounted_price + item2.discounted_price) / 2
        if avg_price > 0:
            price_similarity = max(0, 1 - (price_diff / avg_price))
            score += 0.15 * price_similarity

        # Rating similarity
        rating_diff = abs(item1.ratings - item2.ratings)
        rating_similarity = 1 - (rating_diff / 4)  # Max diff is 4
        score += 0.1 * rating_similarity

        return score

    def get_similar_items(self, base_item, top_n=10):
        """
        Find items similar to the base item.

        Returns: List of (ChefProduct, similarity_score) tuples
        """
        all_items = ChefProduct.objects.exclude(id=base_item.id)
        similarities = []

        for item in all_items:
            similarity = self.calculate_item_similarity(base_item, item)
            if similarity > 0.3:  # Threshold
                similarities.append((item, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_n]

    def get_recommendations_from_history(self, top_n=10):
        """
        Recommend items based on user's purchase and interaction history.

        Returns: QuerySet of recommended ChefProduct objects
        """
        if not self.user:
            return ChefProduct.objects.none()

        # Get user's order history
        user_purchased = OrderPlaced.objects.filter(user=self.user).order_by('-ordered_date')[:5]

        if not user_purchased:
            # Fallback to recently viewed items
            recent_views = UserInteraction.objects.filter(
                user=self.user,
                interaction_type='view'
            ).order_by('-timestamp')[:3]

            if not recent_views:
                return ChefProduct.objects.none()

            base_items = [view.chef_product for view in recent_views if view.chef_product]
        else:
            base_items = [order.product for order in user_purchased]

        # Find similar items for each base item
        product_scores = defaultdict(float)

        for base_item in base_items:
            similar_items = self.get_similar_items(base_item, top_n=5)
            for item, score in similar_items:
                product_scores[item.id] += score

        # Sort by score
        sorted_products = sorted(
            product_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n]

        product_ids = [pid for pid, _ in sorted_products]
        return ChefProduct.objects.filter(id__in=product_ids)


class HybridRecommender:
    """
    Hybrid Recommendation System combining multiple strategies:

    1. Collaborative Filtering (40% weight)
    2. Content-Based Filtering (30% weight)
    3. Popularity-Based (20% weight)
    4. Profile-Based (10% weight)

    Handles cold-start problem with fallback strategies.
    """

    def __init__(self, user):
        self.user = user
        self.collaborative = CollaborativeFiltering(user)
        self.content_based = ContentBasedFiltering(user)

    def get_popularity_based(self, top_n=10):
        """
        Get popular items based on order count and ratings.
        Used as fallback for new users.
        """
        return ChefProduct.objects.annotate(
            order_count=Count('orderplaced')
        ).order_by('-order_count', '-ratings')[:top_n]

    def get_profile_based(self, top_n=10):
        """
        Get recommendations based on user profile preferences.
        Used for cold-start problem.
        """
        try:
            customer = Customer.objects.get(user=self.user)
            return ChefProduct.objects.filter(
                Q(category=customer.category_preference) |
                Q(titleid__cuisine=customer.cuisine_preference)
            ).order_by('-ratings', '-total_orders')[:top_n]
        except Customer.DoesNotExist:
            return self.get_popularity_based(top_n)

    def get_hybrid_recommendations(self, top_n=12):
        """
        Generate hybrid recommendations with weighted scoring.

        Algorithm:
        1. Check user's order history length
        2. If new user (< 3 orders): Use profile + popularity
        3. If returning user: Use all methods with weights
        4. Combine and deduplicate results
        5. Return top N scored items

        Returns: QuerySet of recommended ChefProduct objects
        """
        order_count = OrderPlaced.objects.filter(user=self.user).count()

        # Cold start: New users
        if order_count < 3:
            profile_recs = self.get_profile_based(top_n=8)
            popularity_recs = self.get_popularity_based(top_n=8)

            # Combine and deduplicate
            combined = list(profile_recs) + list(popularity_recs)
            seen = set()
            unique_recs = []
            for item in combined:
                if item.id not in seen:
                    seen.add(item.id)
                    unique_recs.append(item)

            recommendation_type = 'profile'
        else:
            # Returning users: Use all methods
            product_scores = defaultdict(float)

            # Collaborative filtering (40% weight)
            collab_recs = self.collaborative.get_recommendations(top_n=10)
            for idx, item in enumerate(collab_recs):
                product_scores[item.id] += 0.4 * (10 - idx) / 10

            # Content-based (30% weight)
            content_recs = self.content_based.get_recommendations_from_history(top_n=10)
            for idx, item in enumerate(content_recs):
                product_scores[item.id] += 0.3 * (10 - idx) / 10

            # Popularity (20% weight)
            popularity_recs = self.get_popularity_based(top_n=10)
            for idx, item in enumerate(popularity_recs):
                product_scores[item.id] += 0.2 * (10 - idx) / 10

            # Profile-based (10% weight)
            profile_recs = self.get_profile_based(top_n=10)
            for idx, item in enumerate(profile_recs):
                product_scores[item.id] += 0.1 * (10 - idx) / 10

            # Sort by score
            sorted_products = sorted(
                product_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:top_n]

            product_ids = [pid for pid, _ in sorted_products]
            unique_recs = list(ChefProduct.objects.filter(id__in=product_ids))
            recommendation_type = 'hybrid'

        # Log recommendation
        if unique_recs:
            RecommendationLog.objects.create(
                user=self.user,
                recommended_products=[item.id for item in unique_recs],
                recommendation_type=recommendation_type
            )

        return unique_recs[:top_n]


def get_recommendations_for_user(user, recommendation_type='hybrid', top_n=12):
    """
    Main entry point for getting recommendations.

    Args:
        user: Django User object
        recommendation_type: 'hybrid', 'collaborative', 'content', 'popularity', 'profile'
        top_n: Number of recommendations to return

    Returns:
        QuerySet of recommended ChefProduct objects
    """
    if recommendation_type == 'collaborative':
        engine = CollaborativeFiltering(user)
        return engine.get_recommendations(top_n)

    elif recommendation_type == 'content':
        engine = ContentBasedFiltering(user)
        return engine.get_recommendations_from_history(top_n)

    elif recommendation_type == 'popularity':
        return ChefProduct.objects.annotate(
            order_count=Count('orderplaced')
        ).order_by('-order_count', '-ratings')[:top_n]

    elif recommendation_type == 'profile':
        try:
            customer = Customer.objects.get(user=user)
            return ChefProduct.objects.filter(
                Q(category=customer.category_preference) |
                Q(titleid__cuisine=customer.cuisine_preference)
            ).order_by('-ratings', '-total_orders')[:top_n]
        except Customer.DoesNotExist:
            return ChefProduct.objects.order_by('-ratings')[:top_n]

    else:  # hybrid (default)
        engine = HybridRecommender(user)
        return engine.get_hybrid_recommendations(top_n)
