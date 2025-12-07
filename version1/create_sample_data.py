"""
Sample Data Population Script for Food Recommendation System
Creates realistic food items across multiple cuisines and categories
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FoodRecommendationSystem.settings')
django.setup()

from app.models import Product, ChefProduct
from decimal import Decimal


def create_sample_data():
    """Create sample food products"""

    print("Creating sample food products...")

    # Indian Cuisine
    indian_dishes = [
        {
            'title': 'Butter Chicken',
            'description': 'Creamy tomato-based curry with tender chicken pieces',
            'cuisine': 'Indian',
            'meal_type': 'Dinner',
            'chefs': [
                {'name': 'Ravi Kumar', 'price': 250, 'discount': 220, 'rating': 4.5, 'prep_time': 30, 'category': 'NonVegetarian'},
                {'name': 'Priya Sharma', 'price': 270, 'discount': 240, 'rating': 4.7, 'prep_time': 35, 'category': 'NonVegetarian'},
                {'name': 'Amit Patel', 'price': 230, 'discount': 200, 'rating': 4.3, 'prep_time': 25, 'category': 'NonVegetarian'},
            ]
        },
        {
            'title': 'Paneer Tikka Masala',
            'description': 'Grilled cottage cheese in rich creamy gravy',
            'cuisine': 'Indian',
            'meal_type': 'Dinner',
            'chefs': [
                {'name': 'Neha Singh', 'price': 200, 'discount': 180, 'rating': 4.6, 'prep_time': 25, 'category': 'Vegetarian'},
                {'name': 'Rohit Verma', 'price': 220, 'discount': 190, 'rating': 4.4, 'prep_time': 30, 'category': 'Vegetarian'},
                {'name': 'Anjali Gupta', 'price': 210, 'discount': 185, 'rating': 4.5, 'prep_time': 28, 'category': 'Vegetarian'},
            ]
        },
        {
            'title': 'Biryani',
            'description': 'Fragrant rice dish with aromatic spices',
            'cuisine': 'Indian',
            'meal_type': 'Lunch',
            'chefs': [
                {'name': 'Mohammed Ali', 'price': 300, 'discount': 280, 'rating': 4.8, 'prep_time': 45, 'category': 'NonVegetarian'},
                {'name': 'Fatima Khan', 'price': 280, 'discount': 260, 'rating': 4.6, 'prep_time': 40, 'category': 'NonVegetarian'},
                {'name': 'Arjun Reddy', 'price': 250, 'discount': 220, 'rating': 4.4, 'prep_time': 42, 'category': 'Vegetarian'},
            ]
        },
        {
            'title': 'Dal Makhani',
            'description': 'Slow-cooked black lentils in creamy tomato gravy',
            'cuisine': 'Indian',
            'meal_type': 'Dinner',
            'chefs': [
                {'name': 'Sunita Devi', 'price': 150, 'discount': 130, 'rating': 4.5, 'prep_time': 20, 'category': 'Vegetarian'},
                {'name': 'Rajesh Kumar', 'price': 160, 'discount': 140, 'rating': 4.3, 'prep_time': 22, 'category': 'Vegetarian'},
            ]
        },
        {
            'title': 'Tandoori Chicken',
            'description': 'Marinated chicken cooked in clay oven',
            'cuisine': 'Indian',
            'meal_type': 'Dinner',
            'chefs': [
                {'name': 'Vikram Singh', 'price': 280, 'discount': 250, 'rating': 4.7, 'prep_time': 35, 'category': 'NonVegetarian'},
                {'name': 'Harpreet Kaur', 'price': 300, 'discount': 270, 'rating': 4.8, 'prep_time': 38, 'category': 'NonVegetarian'},
            ]
        },
        {
            'title': 'Chole Bhature',
            'description': 'Spicy chickpea curry with fried bread',
            'cuisine': 'Indian',
            'meal_type': 'BreakFast',
            'chefs': [
                {'name': 'Ramesh Goyal', 'price': 120, 'discount': 100, 'rating': 4.4, 'prep_time': 20, 'category': 'Vegetarian'},
                {'name': 'Meena Jain', 'price': 130, 'discount': 110, 'rating': 4.5, 'prep_time': 22, 'category': 'Vegetarian'},
            ]
        },
    ]

    # Chinese Cuisine
    chinese_dishes = [
        {
            'title': 'Hakka Noodles',
            'description': 'Stir-fried noodles with vegetables and sauce',
            'cuisine': 'Chinese',
            'meal_type': 'Lunch',
            'chefs': [
                {'name': 'Chen Wei', 'price': 180, 'discount': 160, 'rating': 4.4, 'prep_time': 18, 'category': 'Vegetarian'},
                {'name': 'Li Ming', 'price': 200, 'discount': 180, 'rating': 4.5, 'prep_time': 20, 'category': 'NonVegetarian'},
                {'name': 'Wang Fang', 'price': 190, 'discount': 170, 'rating': 4.3, 'prep_time': 19, 'category': 'Vegetarian'},
            ]
        },
        {
            'title': 'Manchurian',
            'description': 'Deep-fried dumplings in spicy sauce',
            'cuisine': 'Chinese',
            'meal_type': 'Dinner',
            'chefs': [
                {'name': 'Zhang Yu', 'price': 170, 'discount': 150, 'rating': 4.2, 'prep_time': 22, 'category': 'Vegetarian'},
                {'name': 'Liu Xing', 'price': 190, 'discount': 170, 'rating': 4.4, 'prep_time': 25, 'category': 'NonVegetarian'},
            ]
        },
        {
            'title': 'Fried Rice',
            'description': 'Wok-tossed rice with vegetables and egg',
            'cuisine': 'Chinese',
            'meal_type': 'Lunch',
            'chefs': [
                {'name': 'Chen Wei', 'price': 160, 'discount': 140, 'rating': 4.3, 'prep_time': 15, 'category': 'Vegetarian'},
                {'name': 'Li Ming', 'price': 180, 'discount': 160, 'rating': 4.5, 'prep_time': 18, 'category': 'NonVegetarian'},
            ]
        },
        {
            'title': 'Chilli Chicken',
            'description': 'Spicy chicken in Indo-Chinese sauce',
            'cuisine': 'Chinese',
            'meal_type': 'Dinner',
            'chefs': [
                {'name': 'Wang Fang', 'price': 220, 'discount': 200, 'rating': 4.6, 'prep_time': 25, 'category': 'NonVegetarian'},
                {'name': 'Zhang Yu', 'price': 240, 'discount': 220, 'rating': 4.7, 'prep_time': 28, 'category': 'NonVegetarian'},
            ]
        },
    ]

    # Italian Cuisine
    italian_dishes = [
        {
            'title': 'Margherita Pizza',
            'description': 'Classic pizza with tomato, mozzarella, and basil',
            'cuisine': 'Italian',
            'meal_type': 'Dinner',
            'chefs': [
                {'name': 'Marco Rossi', 'price': 350, 'discount': 320, 'rating': 4.7, 'prep_time': 25, 'category': 'Vegetarian'},
                {'name': 'Giovanni Bianchi', 'price': 380, 'discount': 350, 'rating': 4.8, 'prep_time': 28, 'category': 'Vegetarian'},
                {'name': 'Sofia Romano', 'price': 360, 'discount': 330, 'rating': 4.6, 'prep_time': 26, 'category': 'Vegetarian'},
            ]
        },
        {
            'title': 'Pasta Carbonara',
            'description': 'Creamy pasta with bacon and parmesan',
            'cuisine': 'Italian',
            'meal_type': 'Dinner',
            'chefs': [
                {'name': 'Luigi Ferrari', 'price': 300, 'discount': 280, 'rating': 4.6, 'prep_time': 22, 'category': 'NonVegetarian'},
                {'name': 'Maria Conti', 'price': 320, 'discount': 290, 'rating': 4.7, 'prep_time': 24, 'category': 'NonVegetarian'},
            ]
        },
        {
            'title': 'Penne Arrabbiata',
            'description': 'Spicy tomato sauce with penne pasta',
            'cuisine': 'Italian',
            'meal_type': 'Lunch',
            'chefs': [
                {'name': 'Antonio Ricci', 'price': 250, 'discount': 230, 'rating': 4.4, 'prep_time': 20, 'category': 'Vegetarian'},
                {'name': 'Francesca Marino', 'price': 270, 'discount': 250, 'rating': 4.5, 'prep_time': 22, 'category': 'Vegetarian'},
            ]
        },
        {
            'title': 'Lasagna',
            'description': 'Layered pasta with meat sauce and cheese',
            'cuisine': 'Italian',
            'meal_type': 'Dinner',
            'chefs': [
                {'name': 'Marco Rossi', 'price': 400, 'discount': 370, 'rating': 4.8, 'prep_time': 40, 'category': 'NonVegetarian'},
                {'name': 'Sofia Romano', 'price': 420, 'discount': 380, 'rating': 4.7, 'prep_time': 42, 'category': 'NonVegetarian'},
            ]
        },
    ]

    # Continental Cuisine
    continental_dishes = [
        {
            'title': 'Grilled Chicken Steak',
            'description': 'Juicy grilled chicken with herbs',
            'cuisine': 'Continental',
            'meal_type': 'Dinner',
            'chefs': [
                {'name': 'James Anderson', 'price': 450, 'discount': 420, 'rating': 4.7, 'prep_time': 30, 'category': 'NonVegetarian'},
                {'name': 'Emily White', 'price': 480, 'discount': 450, 'rating': 4.8, 'prep_time': 32, 'category': 'NonVegetarian'},
            ]
        },
        {
            'title': 'Caesar Salad',
            'description': 'Fresh romaine with parmesan and croutons',
            'cuisine': 'Continental',
            'meal_type': 'Lunch',
            'chefs': [
                {'name': 'Sarah Johnson', 'price': 200, 'discount': 180, 'rating': 4.5, 'prep_time': 12, 'category': 'Vegetarian'},
                {'name': 'Michael Brown', 'price': 220, 'discount': 200, 'rating': 4.6, 'prep_time': 15, 'category': 'Vegetarian'},
            ]
        },
        {
            'title': 'Fish and Chips',
            'description': 'Crispy battered fish with french fries',
            'cuisine': 'Continental',
            'meal_type': 'Lunch',
            'chefs': [
                {'name': 'Robert Taylor', 'price': 380, 'discount': 350, 'rating': 4.4, 'prep_time': 25, 'category': 'NonVegetarian'},
                {'name': 'Jennifer Davis', 'price': 400, 'discount': 370, 'rating': 4.5, 'prep_time': 28, 'category': 'NonVegetarian'},
            ]
        },
    ]

    all_dishes = indian_dishes + chinese_dishes + italian_dishes + continental_dishes

    created_count = 0

    for dish_data in all_dishes:
        # Create base product (use first chef's category as default)
        first_chef = dish_data['chefs'][0]
        product, created = Product.objects.get_or_create(
            title=dish_data['title'],
            defaults={
                'description': dish_data['description'],
                'cuisine': dish_data['cuisine'],
                'meal_type': dish_data['meal_type'],
                'category': first_chef['category'],
            }
        )

        if created:
            print(f"  Created product: {product.title}")

        # Create chef variants
        for chef_data in dish_data['chefs']:
            chef_product, created = ChefProduct.objects.get_or_create(
                titleid=product,
                chef_name=chef_data['name'],
                defaults={
                    'category': chef_data['category'],
                    'meal_type': dish_data['meal_type'],
                    'selling_price': chef_data['price'],
                    'discounted_price': chef_data['discount'],
                    'description': dish_data['description'],
                    'ratings': int(chef_data['rating']),
                    'preparation_time': chef_data['prep_time'],
                }
            )

            if created:
                created_count += 1

    print(f"\n✓ Successfully created {created_count} chef products!")
    print(f"✓ Total products: {Product.objects.count()}")
    print(f"✓ Total chef variants: {ChefProduct.objects.count()}")


if __name__ == '__main__':
    create_sample_data()
