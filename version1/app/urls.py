from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and main pages
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.search_view, name='search'),

    # Product browsing
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<str:cuisine>/', views.ProductListView.as_view(), name='product-list-cuisine'),
    path('dish/<int:pk>/', views.DishVariantsView.as_view(), name='dish-variants'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    # Cart operations
    path('cart/', views.show_cart, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/update/<int:cart_id>/', views.update_cart, name='update-cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove-cart'),

    # Checkout and orders
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),

    # User authentication
    path('register/', views.CustomerRegistrationView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # User profile
    path('profile/', views.profile_view, name='profile-view'),
    path('profile/edit/', views.ProfileFormView.as_view(), name='profile-edit'),
]
