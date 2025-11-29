from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

"""
Enhanced Models for ML-Based Food Recommendation System
Microsoft Engage 2022 - Food Ordering Platform

Models:
    - Customer: User profile with preferences for personalized recommendations
    - Product: Food items with attributes for content-based filtering
    - ChefProduct: Chef-specific product variants with pricing and ratings
    - Cart: Shopping cart management
    - OrderPlaced: Order history for collaborative filtering
    - UserInteraction: Track user behavior for ML recommendations
    - RecommendationLog: Track recommendation performance
"""

# Choices for categorical fields
CUISINE_CHOICES = (
    ('Indian', 'Indian'),
    ('Chinese', 'Chinese'),
    ('Italian', 'Italian'),
    ('Continental', 'Continental'),
)

CATEGORY_CHOICES = (
    ('Vegetarian', 'Vegetarian'),
    ('NonVegetarian', 'Non-Vegetarian'),
)

MEAL_TYPE_CHOICES = (
    ('BreakFast', 'Breakfast'),
    ('Lunch', 'Lunch'),
    ('Dinner', 'Dinner'),
    ('Snacks', 'Snacks'),
)

INTERACTION_CHOICES = (
    ('view', 'View'),
    ('click', 'Click'),
    ('add_to_cart', 'Add to Cart'),
    ('purchase', 'Purchase'),
)


class Customer(models.Model):
    """
    Stores user profile information for personalized recommendations.
    Used in collaborative filtering to find similar users.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category_preference = models.CharField(
        choices=CATEGORY_CHOICES,
        max_length=25,
        default="Vegetarian",
        help_text="Dietary preference for profile-based recommendations"
    )
    cuisine_preference = models.CharField(
        choices=CUISINE_CHOICES,
        max_length=50,
        default="Indian",
        help_text="Cuisine preference for content-based filtering"
    )
    mobile = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    class Meta:
        verbose_name_plural = "Customers"


class Product(models.Model):
    """
    Base product model representing food items.
    Attributes used for content-based filtering and similarity calculations.
    """
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    meal_type = models.CharField(choices=MEAL_TYPE_CHOICES, max_length=25)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=25)
    cuisine = models.CharField(choices=CUISINE_CHOICES, max_length=50)
    product_image = models.ImageField(upload_to='productimg')
    popularity_score = models.FloatField(default=0.0, help_text="Calculated based on orders and views")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def update_popularity(self):
        """Calculate popularity score based on interactions and orders"""
        order_count = OrderPlaced.objects.filter(product__titleid=self).count()
        view_count = UserInteraction.objects.filter(
            product=self,
            interaction_type='view'
        ).count()
        # Simple popularity formula
        self.popularity_score = (order_count * 2) + (view_count * 0.1)
        self.save()

    class Meta:
        verbose_name_plural = "Products"
        ordering = ['-popularity_score']


class ChefProduct(models.Model):
    """
    Chef-specific product variants with pricing and ratings.
    Used for price-based and rating-based recommendations.
    """
    titleid = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='chef_variants')
    chef_name = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    preparation_time = models.FloatField(help_text="Time in minutes")
    description = models.TextField()
    ratings = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    meal_type = models.CharField(choices=MEAL_TYPE_CHOICES, max_length=19)
    product_image = models.ImageField(upload_to='chefproductimg')
    total_orders = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def product_name(self):
        return self.titleid.title

    @property
    def cuisine(self):
        return self.titleid.cuisine

    def __str__(self):
        return f"{self.titleid.title} by {self.chef_name}"

    class Meta:
        verbose_name_plural = "Chef Products"
        ordering = ['-ratings', '-total_orders']


class Cart(models.Model):
    """Shopping cart for authenticated users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(ChefProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s cart - {self.product.product_name}"

    @property
    def total_price(self):
        return self.product.discounted_price * self.quantity

    class Meta:
        verbose_name_plural = "Cart Items"


class OrderPlaced(models.Model):
    """
    Order history - critical for collaborative filtering.
    Used to find similar users and generate recommendations.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(ChefProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    @property
    def total_price(self):
        return self.product.discounted_price * self.quantity

    class Meta:
        verbose_name_plural = "Orders Placed"
        ordering = ['-ordered_date']


class UserInteraction(models.Model):
    """
    Track user interactions for ML recommendation improvements.
    Used to understand user behavior and preferences.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    chef_product = models.ForeignKey(ChefProduct, on_delete=models.CASCADE, null=True, blank=True)
    interaction_type = models.CharField(choices=INTERACTION_CHOICES, max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        user_str = self.user.username if self.user else "Anonymous"
        return f"{user_str} - {self.interaction_type} - {self.product.title}"

    class Meta:
        verbose_name_plural = "User Interactions"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'interaction_type']),
            models.Index(fields=['product', 'interaction_type']),
        ]


class RecommendationLog(models.Model):
    """
    Log recommendations shown to users.
    Used for A/B testing and improving recommendation accuracy.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommended_products = models.JSONField(help_text="List of product IDs recommended")
    recommendation_type = models.CharField(
        max_length=50,
        choices=(
            ('collaborative', 'Collaborative Filtering'),
            ('content_based', 'Content-Based'),
            ('hybrid', 'Hybrid'),
            ('popularity', 'Popularity-Based'),
            ('profile', 'Profile-Based'),
        )
    )
    shown_at = models.DateTimeField(auto_now_add=True)
    clicked = models.BooleanField(default=False)
    clicked_product_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Recommendation for {self.user.username} - {self.recommendation_type}"

    class Meta:
        verbose_name_plural = "Recommendation Logs"
        ordering = ['-shown_at']
