from random import choices
from django import forms
from BackOfficeApp.models.customer.models import *

class CustomerRegistrationForm(forms.ModelForm):
  class Meta:
    model = Customer
    fields = "__all__"
    widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Enter First Name Here',
                 'class':'form-control form-control-user' }),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Enter Last Name Here','class':'form-control form-control-user'}),
            'id_number': forms.TextInput(
                attrs={'placeholder': 'Enter ID Number Here','class':'form-control form-control-user'}),
            'cell_phone_number': forms.TextInput(
                attrs={'placeholder': 'Enter CellPhone Number Here','class':'form-control form-control-user'}),
           
            'email': forms.EmailInput(
                attrs={'placeholder': 'Enter Email Address Here','class':'form-control form-control-user'}),
            'home_address': forms.Textarea(
                attrs={'placeholder': 'Enter Home Address Here', 'class': 'form-text-area form-control'}),
            
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
   

class CustomerAssetForm(forms.ModelForm):
  class Meta:
    model = CustomerAsset
    fields =  ('customer',)
    
        
    error_messages = {
            'customer': {
                'required':'Customer is required.'
            }

  }
   