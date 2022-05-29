from django import forms 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from .models import Customer

# form for registration
class CustomerRegistrationForm(UserCreationForm):
    password1 =forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 =forms.CharField(label='Confirm Password (again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email =forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User 
        fields = ['username','email','password1','password2']
        labels={'email':'Email'}
        widgets={'username':forms.TextInput(attrs={'class' :'form-control'})}

# login form
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password = forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))



class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model= Customer
        fields = ['name','Category','prefers','mobile','machineid']
        widgets={'name':forms.TextInput(attrs={'class':'form-control'}),'Category':forms.Select(attrs={'class':'form-control'}),'prefers':forms.Select(attrs={'class':'form-control'}),'mobile':forms.NumberInput(attrs={'class':'form-control'}),'machineid':forms.TextInput(attrs={'class':'form-control'})}