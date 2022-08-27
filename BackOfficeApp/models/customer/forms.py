from django import forms
from BackOfficeApp.models.customer.models import *

class CustomerRegistrationForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = "__all__"
    widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Enter First Name Here' }),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Enter Last Name Here'}),
            'id_number': forms.TextInput(
                attrs={'placeholder': 'Enter ID Number Here'}),
            'cell_phone_number': forms.TextInput(
                attrs={'placeholder': 'Enter CellPhone Number Here'}),
            
            'email': forms.EmailInput(
                attrs={'placeholder': 'Enter Email Address Here'}),
            'home_address': forms.Textarea(
                attrs={'placeholder': 'Enter Home Address Here', 'class': 'form-text-area'}),
            
    }
        
    error_messages = {
            'first_name': {
                'required':'First Name is required.'
            },
            'last_name': {
                'required':'Last Name is required.'
            },
            'id_number': {
                'required':'ID Number is required.'
            },
            'cell_phone_numbe': {
                'required':'Cell Phone Number is required.'
            },
            'home_address': {
                'required':'Home Address is required.'
            },
            'email': {
                'required':'Email Address is required.'
            },
  }
   