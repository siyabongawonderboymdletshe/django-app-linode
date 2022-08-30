from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
  class Meta:
    model = User
    fields =  ('username','password')
    widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': 'Enter Username Here','class':'form-control form-control-user' }),
            'password': forms.PasswordInput(
                attrs={'placeholder': 'Enter Password','class':'form-control form-control-user' }),
            
        }
        
    error_messages = {
            'username': {
                'required':'Username is required.'
            },
            'password': {
                'required':'Password is required.'
            }
        } 