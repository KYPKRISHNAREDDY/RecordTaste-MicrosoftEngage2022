from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

"""
 Created 5 Models :
                  "Customer" - stores Profile details of Customer 
                  "Product" - stores Dish details 
                  "Chefs_Preparing_Product"- stores Details of Dishes cooked by different Cheffs
                  "Cart" - Stores details of dishes that we added to cart
                  "OrderPlaced"- stores Details of Orders that User Made  payment for
"""


Prefered_choices=(
    
    ('Chinese','Chinese'),
    ('Italian','Italian'),
    ('Indian','Indian'),
    ('others','others'),
    
)

CATEGORY_CHOICES = (
 ('Vegetarian', 'Vegetarian'),
 ('NonVegetarian', 'NonVegetarian'),
)

TypeFood_CHOICES = (
 ('BreakFast', 'BreakFast'),
 ('Lunch', 'Lunch'),
 ('Dinner', 'Dinner'),
 ('Refreshers', 'Refreshers'),
)



class Customer(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=200)
  Category = models.CharField(choices=CATEGORY_CHOICES,max_length=25,default="Vegetarian")
  prefers=models.CharField(choices=Prefered_choices,max_length=50,default="Indian")
  mobile=models.PositiveIntegerField(blank=True,null=True )
  machineid=models.CharField(blank=True,null=True,max_length=10)


  def __str__(self):
   return str(self.id)




class Product(models.Model):
 title = models.CharField(max_length=100,unique=True)
 description = models.TextField()
 type_food = models.CharField(choices=TypeFood_CHOICES,max_length=25)
 category = models.CharField( choices=CATEGORY_CHOICES, max_length=25)
 region=models.CharField(choices=Prefered_choices,max_length=50)
 product_image = models.ImageField(upload_to='productimg')

 def __str__(self):
  return str(self.id)

 def name(self):
   return self.title

    
class Chefs_Preparing_Product(models.Model):
 titleid = models.ForeignKey(Product,on_delete=models.CASCADE)
 chef_name=models.CharField(max_length=100)
 selling_price = models.FloatField()
 discounted_price = models.FloatField()
 timeTakesForPreparing=models.FloatField()
 description = models.TextField()
 ratings=models.PositiveIntegerField(default=1)
 category = models.CharField( choices=CATEGORY_CHOICES, max_length=20)
 type_food = models.CharField(choices=TypeFood_CHOICES,max_length=19)
 product_image = models.ImageField(upload_to='Chefproductimg')
 
#  properties for obtaining data
 def getCategory(self):
   return str(self.category)

 def getTypeFood(self):
   return str(self.type_food)

 def getChefName(self):
   return str(self.chef_name)

 def getcategory(self):
   return str(self.category)
  
 def getratings(self):
    return int(self.ratings)
  
 def getprice(self):
    return int(self.discounted_price)

 @property
 def pdtname(self):
     return self.titleid.title
  


 def get_time(self):
     return self.timeTakesForPreparing





 def __str__(self):
  return str(self.id)



class Cart(models.Model):
 user = models.ForeignKey(User, on_delete=models.CASCADE)
 customer = models.ForeignKey(Customer, on_delete=models.CASCADE,blank=True,null=True)
 product = models.ForeignKey(Chefs_Preparing_Product, on_delete=models.CASCADE)
 product_name = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)



 def pdtname(self):
   return self.product_name.pk
  
 def __str__(self):
   return str(self.id)

  

  



class OrderPlaced(models.Model):
 user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
 customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
 product = models.ForeignKey(Chefs_Preparing_Product, on_delete=models.CASCADE)
 product_name = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
 ordered_date = models.DateTimeField(auto_now_add=True)

 def price(self):
   return int(self.product.discounted_price)
