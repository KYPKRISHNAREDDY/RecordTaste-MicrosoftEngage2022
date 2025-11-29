from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from .models import (
    Customer, Product, ChefProduct, Cart,
    OrderPlaced, UserInteraction, RecommendationLog
)
from .forms import CustomerRegistrationForm, CustomerProfileForm
from .recommendation_engine import get_recommendations_for_user, HybridRecommender
from .utils import log_user_interaction


class HomeView(View):
    """
    Home page with personalized ML-based recommendations.

    For authenticated users:
    - Shows hybrid recommendations (collaborative + content-based + profile)
    - Logs user interactions
    - Displays personalized content

    For anonymous users:
    - Shows popular items
    - Categorized product listings
    """

    def get(self, request):
        context = {}
        context['totalitem'] = 0

        # Category-wise products for browsing
        context['vegetarian'] = Product.objects.filter(category='Vegetarian')[:8]
        context['non_vegetarian'] = Product.objects.filter(category='NonVegetarian')[:8]
        context['indian'] = Product.objects.filter(cuisine='Indian')[:8]
        context['chinese'] = Product.objects.filter(cuisine='Chinese')[:6]
        context['italian'] = Product.objects.filter(cuisine='Italian')[:6]

        if request.user.is_authenticated:
            # Cart count
            context['totalitem'] = Cart.objects.filter(user=request.user).count()

            # ML-based personalized recommendations
            try:
                recommender = HybridRecommender(request.user)
                context['ml_recommendations'] = recommender.get_hybrid_recommendations(top_n=12)

                # Profile-based quick recommendations
                customer = Customer.objects.get(user=request.user)
                context['profile_recommendations'] = ChefProduct.objects.filter(
                    Q(category=customer.category_preference) |
                    Q(titleid__cuisine=customer.cuisine_preference)
                ).order_by('-ratings')[:6]

                # Order history based recommendations
                recent_orders = OrderPlaced.objects.filter(
                    user=request.user
                ).order_by('-ordered_date')[:3]

                if recent_orders:
                    context['has_order_history'] = True
                    context['order_history_recommendations'] = recommender.content_based.get_recommendations_from_history(top_n=6)

            except Customer.DoesNotExist:
                # User hasn't filled profile yet
                context['ml_recommendations'] = ChefProduct.objects.order_by('-ratings', '-total_orders')[:12]
                context['profile_incomplete'] = True

        else:
            # For anonymous users: show popular items
            context['ml_recommendations'] = ChefProduct.objects.annotate(
                order_count=Count('orderplaced')
            ).order_by('-order_count', '-ratings')[:12]

        return render(request, 'app/home.html', context)


class ProductListView(View):
    """
    Product listing page with filters and search.
    Tracks user interactions for ML improvement.
    """

    def get(self, request, cuisine=None):
        context = {}
        context['totalitem'] = 0

        if request.user.is_authenticated:
            context['totalitem'] = Cart.objects.filter(user=request.user).count()

        # Get filter parameters
        category = request.GET.get('category')
        price_range = request.GET.get('price')
        rating_filter = request.GET.get('rating')
        meal_type = request.GET.get('meal_type')
        prep_time = request.GET.get('prep_time')

        # Base queryset
        products = ChefProduct.objects.all()

        # Apply filters
        if category:
            products = products.filter(category=category)

        if price_range == 'below100':
            products = products.filter(discounted_price__lt=100)
        elif price_range == 'above100':
            products = products.filter(discounted_price__gte=100)

        if rating_filter:
            products = products.filter(ratings__gte=int(rating_filter))

        if meal_type:
            products = products.filter(meal_type=meal_type)

        if prep_time == 'quick':
            products = products.filter(preparation_time__lt=30)
        elif prep_time == 'medium':
            products = products.filter(preparation_time__range=(30, 60))
        elif prep_time == 'long':
            products = products.filter(preparation_time__gt=60)

        # Cuisine filter from URL
        if cuisine:
            base_products = Product.objects.filter(cuisine=cuisine)
            products = products.filter(titleid__in=base_products)
            context['cuisine'] = cuisine

        context['products'] = products.order_by('-ratings', '-total_orders')
        context['total_count'] = products.count()

        return render(request, 'app/product_list.html', context)


class ProductDetailView(View):
    """
    Detailed product view with item-specific recommendations.
    Uses content-based filtering to show similar items.
    """

    def get(self, request, pk):
        context = {}
        product = get_object_or_404(ChefProduct, pk=pk)
        context['product'] = product
        context['totalitem'] = 0

        # Log interaction
        if request.user.is_authenticated:
            context['totalitem'] = Cart.objects.filter(user=request.user).count()
            log_user_interaction(request.user, product.titleid, 'view', chef_product=product)
        else:
            log_user_interaction(None, product.titleid, 'view', chef_product=product, session_id=request.session.session_key)

        # Content-based recommendations (similar items)
        from .recommendation_engine import ContentBasedFiltering
        cbf = ContentBasedFiltering()
        similar_items = cbf.get_similar_items(product, top_n=8)
        context['similar_items'] = [item for item, score in similar_items]

        # Same chef's other products
        context['chef_products'] = ChefProduct.objects.filter(
            chef_name=product.chef_name
        ).exclude(id=product.id).order_by('-ratings')[:6]

        # Same category products
        context['category_products'] = ChefProduct.objects.filter(
            category=product.category,
            titleid__cuisine=product.titleid.cuisine
        ).exclude(id=product.id).order_by('-ratings')[:6]

        return render(request, 'app/product_detail.html', context)


class DishVariantsView(View):
    """
    Show all chef variants for a specific dish.
    Helps users compare different chef versions of the same dish.
    """

    def get(self, request, pk):
        context = {}
        base_product = get_object_or_404(Product, pk=pk)
        context['product'] = base_product
        context['totalitem'] = 0

        if request.user.is_authenticated:
            context['totalitem'] = Cart.objects.filter(user=request.user).count()
            log_user_interaction(request.user, base_product, 'view')

        # Get all chef variants
        context['chef_variants'] = ChefProduct.objects.filter(
            titleid=base_product
        ).order_by('-ratings', '-total_orders')

        return render(request, 'app/dish_variants.html', context)


@login_required
def add_to_cart(request):
    """
    Add product to cart and log interaction.
    Requires authentication.
    """
    product_id = request.GET.get('prod_id')

    if not product_id:
        messages.error(request, "Invalid product")
        return redirect('home')

    product = get_object_or_404(ChefProduct, id=product_id)

    # Get or create customer profile
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={'name': request.user.username}
    )

    # Check if already in cart
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'customer': customer, 'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Increased quantity of {product.product_name}")
    else:
        messages.success(request, f"Added {product.product_name} to cart")

    # Log interaction
    log_user_interaction(request.user, product.titleid, 'add_to_cart', chef_product=product)

    return redirect('cart')


@login_required
def show_cart(request):
    """
    Display cart with total calculation and recommendations.
    Shows items user might also like based on cart contents.
    """
    context = {}
    cart_items = Cart.objects.filter(user=request.user)
    context['cart_items'] = cart_items
    context['totalitem'] = cart_items.count()

    if cart_items.exists():
        total_amount = sum(item.total_price for item in cart_items)
        context['total_amount'] = total_amount

        # Recommend items based on cart contents
        cart_products = [item.product for item in cart_items]
        if cart_products:
            from .recommendation_engine import ContentBasedFiltering
            cbf = ContentBasedFiltering()

            similar_items = []
            for cart_product in cart_products[:2]:  # Check first 2 items
                similar = cbf.get_similar_items(cart_product, top_n=4)
                similar_items.extend([item for item, score in similar])

            # Remove duplicates and items already in cart
            cart_product_ids = [item.product.id for item in cart_items]
            unique_similar = []
            seen = set()
            for item in similar_items:
                if item.id not in seen and item.id not in cart_product_ids:
                    seen.add(item.id)
                    unique_similar.append(item)

            context['you_may_also_like'] = unique_similar[:6]
    else:
        context['cart_empty'] = True

    return render(request, 'app/cart.html', context)


@login_required
def update_cart(request, cart_id):
    """Update cart item quantity"""
    action = request.GET.get('action')
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "Quantity increased")
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, "Quantity decreased")
        else:
            cart_item.delete()
            messages.success(request, "Item removed from cart")

    return redirect('cart')


@login_required
def remove_from_cart(request, cart_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    product_name = cart_item.product.product_name
    cart_item.delete()
    messages.success(request, f"Removed {product_name} from cart")
    return redirect('cart')


@login_required
def checkout(request):
    """
    Process checkout and create orders.
    Move cart items to order history for ML training.
    """
    customer = get_object_or_404(Customer, user=request.user)
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty")
        return redirect('cart')

    # Create orders
    for cart_item in cart_items:
        OrderPlaced.objects.create(
            user=request.user,
            customer=customer,
            product=cart_item.product,
            quantity=cart_item.quantity
        )

        # Update product statistics
        cart_item.product.total_orders += cart_item.quantity
        cart_item.product.save()

        # Log purchase interaction
        log_user_interaction(
            request.user,
            cart_item.product.titleid,
            'purchase',
            chef_product=cart_item.product
        )

    # Clear cart
    cart_items.delete()

    messages.success(request, "Order placed successfully!")
    return redirect('orders')


@login_required
def orders(request):
    """
    Display order history with recommendations based on past orders.
    Uses collaborative filtering for personalized suggestions.
    """
    context = {}
    order_list = OrderPlaced.objects.filter(user=request.user).order_by('-ordered_date')
    context['orders'] = order_list
    context['totalitem'] = Cart.objects.filter(user=request.user).count()

    if order_list.exists():
        # ML-based recommendations from order history
        recommender = HybridRecommender(request.user)
        context['recommended_items'] = recommender.get_hybrid_recommendations(top_n=8)

        # Calculate total spent
        total_spent = sum(order.total_price for order in order_list)
        context['total_spent'] = total_spent
        context['total_orders'] = order_list.count()

    return render(request, 'app/orders.html', context)


@login_required
def profile_view(request):
    """Display user profile"""
    context = {}
    context['totalitem'] = Cart.objects.filter(user=request.user).count()

    try:
        customer = Customer.objects.get(user=request.user)
        context['customer'] = customer
    except Customer.DoesNotExist:
        context['profile_incomplete'] = True

    return render(request, 'app/profile_view.html', context)


class CustomerRegistrationView(View):
    """User registration with Django auth"""

    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/registration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        return render(request, 'app/registration.html', {'form': form})


class ProfileFormView(View):
    """
    User profile creation/update.
    Profile data is crucial for profile-based recommendations.
    """

    def get(self, request):
        context = {}
        context['totalitem'] = Cart.objects.filter(user=request.user).count()

        try:
            customer = Customer.objects.get(user=request.user)
            form = CustomerProfileForm(instance=customer)
            context['editing'] = True
        except Customer.DoesNotExist:
            form = CustomerProfileForm()
            context['editing'] = False

        context['form'] = form
        return render(request, 'app/profile_form.html', context)

    def post(self, request):
        context = {}

        try:
            customer = Customer.objects.get(user=request.user)
            form = CustomerProfileForm(request.POST, instance=customer)
        except Customer.DoesNotExist:
            form = CustomerProfileForm(request.POST)

        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile-view')

        context['form'] = form
        return render(request, 'app/profile_form.html', context)


def search_view(request):
    """
    Search functionality with ML-enhanced results.
    Logs search queries for future improvements.
    """
    query = request.GET.get('q', '')
    context = {}
    context['totalitem'] = 0
    context['query'] = query

    if request.user.is_authenticated:
        context['totalitem'] = Cart.objects.filter(user=request.user).count()

    if query:
        # Search in products and chef products
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(cuisine__icontains=query)
        )

        chef_products = ChefProduct.objects.filter(
            Q(titleid__in=products) |
            Q(chef_name__icontains=query) |
            Q(description__icontains=query)
        ).order_by('-ratings', '-total_orders')

        context['results'] = chef_products
        context['result_count'] = chef_products.count()
    else:
        context['results'] = []
        context['result_count'] = 0

    return render(request, 'app/search.html', context)
