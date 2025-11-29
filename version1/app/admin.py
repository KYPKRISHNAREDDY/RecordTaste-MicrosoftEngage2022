from django.contrib import admin
from .models import (
    Customer, Product, ChefProduct, Cart,
    OrderPlaced, UserInteraction, RecommendationLog
)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'category_preference', 'cuisine_preference', 'created_at']
    list_filter = ['category_preference', 'cuisine_preference', 'created_at']
    search_fields = ['name', 'user__username', 'mobile']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'cuisine', 'category', 'meal_type', 'popularity_score', 'created_at']
    list_filter = ['cuisine', 'category', 'meal_type']
    search_fields = ['title', 'description']
    readonly_fields = ['popularity_score', 'created_at']
    ordering = ['-popularity_score']


@admin.register(ChefProduct)
class ChefProductAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'product_name', 'chef_name', 'discounted_price',
        'ratings', 'total_orders', 'category', 'meal_type'
    ]
    list_filter = ['category', 'meal_type', 'ratings', 'created_at']
    search_fields = ['titleid__title', 'chef_name', 'description']
    readonly_fields = ['total_orders', 'created_at']
    ordering = ['-ratings', '-total_orders']

    def product_name(self, obj):
        return obj.titleid.title
    product_name.short_description = 'Product'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'total_price', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'product__titleid__title']
    readonly_fields = ['added_at']

    def total_price(self, obj):
        return f"₹{obj.total_price}"
    total_price.short_description = 'Total Price'


@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'total_price', 'ordered_date']
    list_filter = ['ordered_date', 'product__category', 'product__meal_type']
    search_fields = ['user__username', 'product__titleid__title', 'customer__name']
    readonly_fields = ['ordered_date']
    date_hierarchy = 'ordered_date'

    def total_price(self, obj):
        return f"₹{obj.total_price}"
    total_price.short_description = 'Total Price'


@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'interaction_type', 'timestamp']
    list_filter = ['interaction_type', 'timestamp']
    search_fields = ['user__username', 'product__title']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        # Interactions are created automatically
        return False


@admin.register(RecommendationLog)
class RecommendationLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recommendation_type', 'clicked', 'shown_at']
    list_filter = ['recommendation_type', 'clicked', 'shown_at']
    search_fields = ['user__username']
    readonly_fields = ['shown_at']
    date_hierarchy = 'shown_at'

    def has_add_permission(self, request):
        # Logs are created automatically
        return False


# Custom admin site configuration
admin.site.site_header = "Food Recommendation System - Admin"
admin.site.site_title = "FRS Admin Portal"
admin.site.index_title = "Welcome to Food Recommendation System Administration"
