from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm

urlpatterns = [
    path('', views.ProductView.as_view(),name="home"),
    path('cheff-detail/<int:pk>',views.Cheff_Detail.as_view(),name='cheff-detail'),
    path('product-detail/<int:pk>', views.Product_Detail.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profiledetails/', views.profiledetails, name='profiledetails'),
    path('orders/', views.orders, name='orders'),
    path('Indian/', views.Indian, name='Indian'),
    path('Indian/<slug:data>', views.Indian, name='IndianData'),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

