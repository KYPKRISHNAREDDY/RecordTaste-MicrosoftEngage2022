from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer


class CustomerRegistrationForm(UserCreationForm):
    """
    User registration form with email validation.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose username'
        })
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create password'
        })
    )

    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class CustomerProfileForm(forms.ModelForm):
    """
    Customer profile form for collecting preferences.
    These preferences are used for ML-based recommendations.
    """
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name'
        })
    )

    category_preference = forms.ChoiceField(
        choices=[
            ('Vegetarian', 'Vegetarian'),
            ('NonVegetarian', 'Non-Vegetarian')
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Food Preference'
    )

    cuisine_preference = forms.ChoiceField(
        choices=[
            ('Indian', 'Indian'),
            ('Chinese', 'Chinese'),
            ('Italian', 'Italian'),
            ('Continental', 'Continental')
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Favorite Cuisine'
    )

    mobile = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mobile number (optional)'
        })
    )

    class Meta:
        model = Customer
        fields = ['name', 'category_preference', 'cuisine_preference', 'mobile']

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if mobile and not mobile.isdigit():
            raise forms.ValidationError("Mobile number must contain only digits.")
        if mobile and len(mobile) < 10:
            raise forms.ValidationError("Mobile number must be at least 10 digits.")
        return mobile
