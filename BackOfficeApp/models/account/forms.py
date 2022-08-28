from django import forms
from BackOfficeApp.models.account.models import *

class AccountRegistrationForm(forms.ModelForm):
  class Meta:
    model = Account
    fields =  ('loan_amount','rate', 'number_of_products', 'payment_due_date')
    labels = {
       'loan_amount' : '', 'rate' : '', 'number_of_products' : '', 'payment_due_date' : '',
    }
    widgets = {
            'loan_amount': forms.NumberInput(
                attrs={'placeholder': 'Enter Loan Amount Here','class':'form-control form-control-user' }),
            'rate': forms.NumberInput(
                attrs={'placeholder': 'Enter Rate Here','class':'form-control form-control-user' }),
            'number_of_products': forms.NumberInput(
                attrs={'placeholder': 'Enter Number Of Products Here','class':'form-control form-control-user' }),
            'payment_due_date': forms.DateTimeInput(
                attrs={'placeholder': 'Select Payment Due Date Here','class':'form-control form-control-user',"onfocus":"this.type='date'",
                "onblur":"this.type='text'"  
                })  
        }
        
    error_messages = {
            'loan_amount': {
                'required':'Loan Amount is required.'
            },
            'rate': {
                'required':'Rate is required.'
            },
            'number_of_products': {
                'required':'The Number Of Product is required.'
            },
            'payment_due_date': {
                'required':'The Payment Due Date is required.'
            }
        } 