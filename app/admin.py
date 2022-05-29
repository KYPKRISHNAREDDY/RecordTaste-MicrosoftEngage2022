from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import (
 Customer,
 Product,
 Chefs_Preparing_Product,
 Cart,
 OrderPlaced
)

# registering models that we have created in models.py

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
 list_display = ['id', 'user', 'name', 'Category','prefers','mobile','machineid']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
 list_display = ['id', 'title', 'description', 'type_food', 'category', 'region','product_image']

@admin.register(Chefs_Preparing_Product)
class Chefs_Preparing_ProductModelAdmin(admin.ModelAdmin):
 list_display = ['id','titleid', 'chef_name','selling_price', 'discounted_price', 'timeTakesForPreparing', 'description', 'ratings', 'category','type_food','product_image']

 def title(self, obj):
  link = reverse("admin:app_product_change", args=[obj.product.pk])
  return format_html('<a href="{}">{}</a>', link, obj.product.title)

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
 list_display = ['id', 'user','customer', 'product','product_name']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
 list_display = ['id', 'user', 'customer', 'product', 'ordered_date','product_name']


 
