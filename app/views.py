from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Chefs_Preparing_Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages

"""
This Product View helps in filetring objects to show on home page
this filters Objects based on Product Model attributes 
and it filters objects based on Whether user logged on or not 
so if user logged in ,On home page We will see some set of items
    if user haven't logged in,we'll see different set of items on homepage
"""
class ProductView(View):
    def get(self,request):
        totalitem=0
        Vegetarian = Product.objects.filter(category='Vegetarian')
        NonVegetarian = Product.objects.filter(category='NonVegetarian')
        Indian = Product.objects.filter(region='Indian')
        Italian = Product.objects.filter(region='Italian')
        Chinese = Product.objects.filter(region='Chinese')
        BreakFast = Product.objects.filter(type_food='BreakFast')
        Lunch = Product.objects.filter(type_food='Lunch')
        dinner = Product.objects.filter(type_food='Dinner')
        Refreshers = Product.objects.filter(type_food='Refreshers')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            user=request.user
            categ=Customer.objects.get(user=user)
            categ_type=categ.Category
            prefer_type=categ.prefers
            Recommendation_categ = Product.objects.filter(category=categ_type)
            Recommendation_prefer= Product.objects.filter(region=prefer_type)
            
            OrderedProducts = [p for p in OrderPlaced.objects.all() if p.user == user] #gives in listform



            return render(request,'app/home.html',{'Recommendation_categ':Recommendation_categ,'Recommendation_prefer':Recommendation_prefer,'Vegetarian':Vegetarian,'NonVegetarian':NonVegetarian,'Indian':Indian,'Italian':Italian,'Chinese':Chinese,'BreakFast':BreakFast,'Lunch':Lunch,'dinner':dinner,'Refreshers':Refreshers,'totalitem':totalitem})         
        else:
            return render(request,'app/home.html',{'Vegetarian':Vegetarian,'NonVegetarian':NonVegetarian,'Indian':Indian,'Italian':Italian,'Chinese':Chinese,'BreakFast':BreakFast,'Lunch':Lunch,'dinner':dinner,'Refreshers':Refreshers})




""" 
This Cheff_Detail gives dish Specific Products
Suppose if you chose idly,this will filter all the idly items cooked by different chefs from Chefs_Preparing_Product model

"""

class Cheff_Detail(View):
    def get(self,request,pk):
        totalitem=0

        product1=Product.objects.get(pk=pk)
        product2=Chefs_Preparing_Product.objects.filter(titleid=pk)
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        
        return render(request,'app/cheff_details.html',{'product1':product1,'product2':product2,'totalitem':totalitem})





""" 
This Product_Detail gives details about the dist that you clicked in Cheff_details page
and here we can add dish to the cart
and it will show the related dishes based on the dish you selected.
Suppose if you chose biryani,
    In recommendation Bar You can see
                - More dishes from the same chef
                - similar priced dishes
                - similar ratings dishes
                - similar category items
                - similar time taking items


"""


class Product_Detail(View):
    def get(self,request,pk):
        totalitem = 0
        product=Chefs_Preparing_Product.objects.get(pk=pk)
        cheff_recommendation=Chefs_Preparing_Product.objects.filter(chef_name=product.getChefName())
        Price_recommendation=Chefs_Preparing_Product.objects.filter(discounted_price__lt=100)
        if product.getprice()>100:
            Price_recommendation=Chefs_Preparing_Product.objects.filter(discounted_price__gt=100)
        Rating_recommendation=Chefs_Preparing_Product.objects.filter(ratings=product.getratings())
        Time_recommendation=Chefs_Preparing_Product.objects.filter(timeTakesForPreparing__lt=product.get_time())
        Type_recommendation=Chefs_Preparing_Product.objects.filter(type_food =product.getTypeFood())
        Category_recommendation=Chefs_Preparing_Product.objects.filter(category =product.getCategory())
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/productdetail.html',{'product':product,'cheff_recommendation':cheff_recommendation,'Price_recommendation':Price_recommendation,'Rating_recommendation':Rating_recommendation,'Time_recommendation':Time_recommendation,'Type_recommendation':Type_recommendation,'Category_recommendation':Category_recommendation,'totalitem':totalitem})




""" 
If user is logged in:
                This add_t0_cart will Identify the productId of dish that you added to the cart
                and will store the dishes details in Cart Model
                and after storing,it will redirect to show cart
else:
        It will show empty cart page if user is not logged in and trying to access the cart page
"""


def add_to_cart(request):
 if request.user.is_authenticated:
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Chefs_Preparing_Product.objects.get(id=product_id)
    item_id= int(''.join(filter(str.isdigit,str(product.titleid))))
    product_name=Product.objects.get(pk=item_id)
    customer=Customer.objects.get(user=user)
    Cart(user=user,customer=customer,product=product,product_name=product_name).save()
    return redirect('/cart')
 else:
    return render(request,'app/emptycart.html')




""" 
If user is logged in:
    This Show_cart shows the items which are in your Cart model
    this will show each dish price 
    and 
    will sum up all dishes prices which are in your cart and 
    displays total_amount you need to pay
    If you Click on payment,it will redirect to Orders Page

"""

def show_cart(request):
    if request.user.is_authenticated:
        totalitems=0
        totalitems= len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user) # gives in  QuerySet form
        amount=0.0
        chef_charges=50.0
        total_amount=0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user] #gives in listform

        if cart_product:
            for p in cart_product:
                amount+= p.product.discounted_price
    
            return render(request, 'app/addtocart.html',{'carts':cart,'amount':amount,'totalitems':totalitems})

        else:
            return render(request,'app/emptycart.html')
    




""" 
This Profile_Detail gives the Logged In user details 
by sending the User object to profiledetials.html file
and in that page we will render out the User details

"""

def profiledetails(request):
    add = Customer.objects.filter(user=request.user)
    totalitems=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/profiledetails.html',{'add':add,'active':'btn-primary','totalitem':totalitem})





"""
This Payment_done gives Dishes which you made payment for
and once you made the payment,the dishes will be removed from cart 
and adds dishes to Order_Placed model
and cart gets emptied after adding dishes to Order_placed model
and redirects to Orders Page
"""
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer = [p for p in Customer.objects.all() if p.user == user]
    customerid=customer[0].id
    cust=Customer.objects.get(id=customerid)
    cart=Cart.objects.filter(user=user)
    
    for c in cart:
        item_id= int(''.join(filter(str.isdigit,str(c.product_name))))
        product_name=Product.objects.get(pk=item_id)
        OrderPlaced(user=user,customer=cust,product=c.product,product_name=product_name).save()
        c.delete()
    return redirect("orders")
    


    

""" 
This Orders will fetch the data from OrdersPlaced Model and 
   shows Dishes which you made payment for
and it will show similar items based on the price of dish that you have ordered lasttime
"""

def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    totalitems=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 # Recommendation Based on Order History
    if op:
        Price_recommendation=Chefs_Preparing_Product.objects.filter(discounted_price__lt=100)
        for o in op:
            if o.price()>100:
                Price_recommendation=Chefs_Preparing_Product.objects.filter(discounted_price__gt=100)
                break
           
        return render(request, 'app/orders.html',{'order_placed':op,'Price_recommendation':Price_recommendation,'totalitems':totalitems})




""" 
This IndianMethod filters the dishes based on option selected by user in NavigationBar
filters objects based on 
                        - Category:Veg,NonVeg
                        - Price : above 100rs,Below 100rs
                        - time  : abouve 1hr ,below 1hr
                        - ratings : with 5star ratings ,>=3Star ratings
                        - type of food : Breakfast,lunch,dinner,Refreshments
                        

"""

def Indian(request,data=None):
    totalitems=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    if data == None:
        items=Chefs_Preparing_Product.objects.filter(ratings=5)
    elif data == 'Vegetarian' or data == 'NonVegetarian':
        items=Chefs_Preparing_Product.objects.filter(category=data)
    elif data == 'below':
        items=Chefs_Preparing_Product.objects.filter(discounted_price__lt=100)
    elif data == 'above':
        items=Chefs_Preparing_Product.objects.filter(discounted_price__gt=100)
    elif data == 'ratingmorethanthree':
        items=Chefs_Preparing_Product.objects.filter(ratings__gt=2)
    elif data == 'timemorethanhour':
        items=Chefs_Preparing_Product.objects.filter(timeTakesForPreparing__gt=60)
    elif data == 'timelessthanhour':
        items=Chefs_Preparing_Product.objects.filter( timeTakesForPreparing__lt=60)
    elif data == 'BreakFast':
        items=Chefs_Preparing_Product.objects.filter(type_food=data)
    elif data == 'Lunch':
        items=Chefs_Preparing_Product.objects.filter(type_food=data)
    elif data == 'Dinner':
        items=Chefs_Preparing_Product.objects.filter(type_food=data)
    elif data == 'Refreshers':
        items=Chefs_Preparing_Product.objects.filter(type_food=data)
    return render(request, 'app/Indian.html',{'items':items,'totalitems':totalitems})




"""
This CustomerRegistrationView renders the registration form page
"""

class CustomerRegistrationView(View):
    def get(self,request):
        form= CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratualtions! Registered Successfully')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})





    """
    This ProfileView Collects user profile details and 
    saves them in Customer Model
    """

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitems=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitems':totalitems})
    
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name = form.cleaned_data['name']
            Category= form.cleaned_data['Category']
            prefers = form.cleaned_data['prefers']
            mobile = form.cleaned_data['mobile']
            machineid=form.cleaned_data['machineid']
            reg=Customer(user=usr,name=name,Category=Category,prefers=prefers,mobile=mobile,machineid=machineid)
            reg.save()
            messages.success(request,'Congratulations!!Profile Updated Successfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

