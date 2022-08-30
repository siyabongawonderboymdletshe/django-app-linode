from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
  class Meta:
    model = User
    fields =  ('first_name', 'last_name','username','password', 'email')
    widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Enter Firstname','class':'form-control form-control-user' }),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Enter Lastname','class':'form-control form-control-user' }),
            'username': forms.TextInput(
                attrs={'placeholder': 'Enter Username','class':'form-control form-control-user' }),
            'email': forms.TextInput(
                attrs={'placeholder': 'Enter Email','class':'form-control form-control-user' }),
            'password': forms.PasswordInput(
                attrs={'placeholder': 'Enter Password','class':'form-control form-control-user' }),
            
    }
    
    error_messages = {
            'first_name': {
                'required':'Firstname is required.'
            },
            'last_name': {
                'required':'Lastname is required.'
            },
            'username': {
                'required':'Username is required.'
            },
            'email': {
                'required':'Email is required.'
            },
            'password': {
                'required':'Password is required.'
            }
    } 