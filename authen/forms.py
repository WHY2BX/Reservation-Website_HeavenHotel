from django import forms
from hotel.models import *

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="First name", 
        max_length=100, 
        widget = forms.TextInput(attrs={'class': 'form-control'})
        )
    
    last_name = forms.CharField(
        label="Last name", 
        max_length=100, 
        widget = forms.TextInput(attrs={'class': 'form-control'})
        )
    
    username = forms.CharField(
        label="Username", 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = {
            
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        }

#----------------
class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old password", 
        max_length=100, 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    new_password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = {
            'old_password',
            'new_password1',
            'new_password2'
        }