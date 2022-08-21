from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django import forms
from django.utils import timezone

GENDER_CHOICES = (  ('MALE', 'MALE'),  ('FEMALE', 'FEMALE'))
class Customer(models.Model):
  
  first_name = models.CharField("First Name", max_length=150, blank=False)
  last_name = models.CharField("Last Name", max_length=150, blank=False)
  email = models.EmailField("Email Address", max_length=150, blank=False)

  id_number = models.CharField("ID Number", max_length=13, validators=[RegexValidator(r'^[0-9]+$'), MinLengthValidator(13)])
  cell_phone_number = models.CharField("Cellphone Number", max_length=10, validators=[RegexValidator(r'^[0-9]+$'), MinLengthValidator(10)])
  gender = models.CharField(max_length=6, choices= GENDER_CHOICES)
  home_address = models.TextField("Home Address", max_length=255, blank=False, default="")

  class Meta:
        ordering = ['first_name', 'last_name']

  def __str__(self):
    return f'{self.first_name} {self.last_name}'


class ProductCategory(models.Model):
  name = models.CharField("Category", max_length=150, blank=False)

class ProductItem(models.Model):
  name = models.CharField("Name", max_length=150, blank=False)
  year = models.IntegerField("Year", blank= False)
  category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
  serial_number = models.CharField("Serial Number", max_length=150, blank=False)
  description = models.TextField("Description", blank=False, default="")

class CustomerAsset(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
  
class Account(models.Model):
  loan_amount = models.DecimalField("Loan Amount", max_digits=13, decimal_places=2, blank= False)
  rate = models.DecimalField("Rate", max_digits=5, decimal_places=2, blank= False)
  created_at = models.DateTimeField("Created Date")
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  
  def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.created_at = timezone.now()
        return super(Account, self).save(*args, **kwargs)
  
  class Meta:
        ordering = ['created_at']

  def __str__(self):
    return f'{self.customer} has a loan of R{self.loan_amount}'
  

  
class AccountItem(models.Model):
  STATUS_CHOICES = (  ('AVAILABLE', 'AVAILABLE'),  ('SOLD', 'SOLD'), ('REMOVED', 'REMOVED'),  ('UNAVAILABLE', 'UNAVAILABLE'))
  market_value = models.BigIntegerField("Market Value", blank= False)
  account = models.ForeignKey(Account, on_delete=models.CASCADE)
  product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
  operative_date = models.DateField("Operative Date", blank= False)
  status = models.CharField(max_length=255, choices= STATUS_CHOICES, default='AVAILABLE')
  updated_at = models.DateTimeField("Updated Date", auto_now=True)
   
class Catalogue(models.Model):
  product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)

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
                attrs={'placeholder': 'Enter Home Address Here'}),
            
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
    
class AccountRegistrationForm(forms.ModelForm):
  class Meta:
    model = Account
    fields =  ('loan_amount','rate')
    widgets = {
            'loan_amount': forms.NumberInput(
                attrs={'placeholder': 'Enter Loan Amount Here' }),
            'rate': forms.NumberInput(
                attrs={'placeholder': 'Enter Rate Here' }),
            
            
        }
        
    error_messages = {
            'loan_amount': {
                'required':'Loan Amount is required.'
            },
            'rate': {
                'required':'Rate is required.'
            }
        } 

class DashboardSession:
  display_template = ''
  add_customer_form = ''
  add_account_form = ''
  add_customer_title = ''
  add_customer_message = ''
  add_customer_message_class = ''
  add_customer_message_action = ''
  add_customer_message_action_hyperlink_text = ''
  add_customer_message_action_hyperlink_url = ''
  add_customer_message_action_hyperlink_url_parameters = ''
  add_customer_post_form_parameters = ''
