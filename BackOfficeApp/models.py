from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django import forms
from django.utils import timezone
import os
from .validators import validate_file_extension

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
  def __str__(self):
    return f'{self.name}'

class ProductItem(models.Model):
  name = models.CharField("Name", max_length=150, blank=False)
  year = models.IntegerField("Year", blank= False)
  serial_number = models.CharField("Serial Number", max_length=150, blank=False)
  category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
  description = models.TextField("Description", blank=False, default="")
  def __str__(self):
    return f'{self.year} {self.name}, with serial number {self.serial_number}'

def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s_%s_%s.%s" % (instance.product_item.name, instance.product_item.year,'productItemId', instance.product_item.id, ext)
    return os.path.join('product_images', filename)

class ProductItemImage(models.Model):
  product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
  image = models.ImageField(upload_to=content_file_name)
  def __str__(self):
    return f'{os.path.basename(self.image.name)}'
  
class CustomerAsset(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
  def __str__(self):
    return f'{self.customer} owns {self.product_item}'
  
class Account(models.Model):
  loan_amount = models.DecimalField("Loan Amount", max_digits=13, decimal_places=2, blank= False)
  rate = models.DecimalField("Rate", max_digits=5, decimal_places=2, blank= False)
  created_at = models.DateTimeField("Created Date")
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  number_of_products = models.IntegerField("Number Of Products", blank= False)
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
  market_value = models.DecimalField("Market Value", max_digits=13, decimal_places=2, blank= False)
  account = models.ForeignKey(Account, on_delete=models.CASCADE)
  product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
  operative_date = models.DateField("Payment Due Date", blank= False)
  status = models.CharField(max_length=255, choices= STATUS_CHOICES, default='AVAILABLE')
  created_at = models.DateTimeField("Created Date", blank= False)
  updated_at = models.DateTimeField("Updated Date")
  def __str__(self):
    return f'{self.account} and product {self.product_item}'

  def save(self, *args, **kwargs):
        if self.id:
            self.updated_at = timezone.now()
        return super(AccountItem, self).save(*args, **kwargs)
   
class Catalogue(models.Model):
  product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.product_item} and ready for auction.' 

class ProductRequest(models.Model):
  account_id = models.IntegerField("Account Id", blank= False)
  hash_value = models.CharField("Request Hash", max_length=255)
  created_at = models.DateTimeField("Created Date", blank= False, auto_now_add = True)
  
  def __str__(self):
    return f'Hash = [{self.hash_value}], Account = {self.account_id}'



#FORMS

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
    
class AccountRegistrationForm(forms.ModelForm):
  class Meta:
    model = Account
    fields =  ('loan_amount','rate', 'number_of_products')
    labels = {
       'loan_amount' : '',
    }
    widgets = {
            'loan_amount': forms.NumberInput(
                attrs={'placeholder': 'Enter Loan Amount Here' }),
            'rate': forms.NumberInput(
                attrs={'placeholder': 'Enter Rate Here' }),

            'number_of_products': forms.NumberInput(
                attrs={'placeholder': 'Enter Number Of Products Here' }),    
            
            
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
            }
        } 

class ProductItemForm(forms.ModelForm):
  class Meta:
    model = ProductItem
    fields = "__all__"
    labels = {
       'name' : '','serial_number' : '','year' : '','description' : '','category' : '',
    }
   
    widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Enter Name Here' }),
            'serial_number': forms.TextInput(
                attrs={'placeholder': 'Enter Serial Number Here'}),
            'year': forms.NumberInput(
                attrs={'placeholder': 'Enter Year Here'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Enter Description Here', 'class': 'form-text-area'}),
            'category': forms.Select(
                attrs={'placeholder': 'Select Category Here', 'class': 'form-category'}),
            
    }
    error_messages = {
            'name': {
                'required':'The Product Name is required.'
            },
            'serial_number': {
                'required':'The Serial Number is required.'
            },
            'year': {
                'required':'The Year is required.'
            },
            'description': {
                'required':'The Description is required.'
            },
            'category': {
                'required':'The Category is required.'
            }
  }
    
class AccountItemForm(forms.ModelForm):
  class Meta:
    model = AccountItem
    fields =  ('market_value','operative_date')
    labels = {
       'market_value' : '','operative_date' : ''
    }
    widgets = {
            'market_value': forms.NumberInput(
                attrs={'placeholder': 'Enter Market Value Here'}),
            'operative_date': forms.DateTimeInput(
                attrs={'placeholder': 'Select Payment Due Date Here',"onfocus":"this.type='date'",
                "onblur":"this.type='text'"  
                })
    }
    error_messages = {
            'market_value': {
                'required':'The Market Value is required.'
            },
            'operative_date': {
                'required':'The Operative Date is required.'
            }
    }

class ProductItemImageForm(forms.ModelForm):
  class Meta:
    model = ProductItemImage
    fields =  ('image',)
    labels = {
       'image' : ''
    }
    widgets = {
            'image': forms.FileInput(
                attrs={'placeholder': 'Select Product Image Here', 'class':'custom-file-input1'} ),
    }
    error_messages = {
            'image': {
                'required':'The Image is required.'
            }
    }

class ProductCategoryForm(forms.ModelForm):
  class Meta:
    model = ProductCategory
    fields = "__all__"
           
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
  add_customer_message_action_hyperlink_url_query_string = ''
  add_customer_post_form_parameters = ''
  add_product_form = ''
  add_product_catagory_form = ''
  add_product_customer_form = ''
  add_account_item_form = ''
  add_product_image_form = ''
  add_number_of_products = ''
  add_product_forms = []
  add_account_item_forms = []
  add_product_image_forms = []
  add_product_forms_list = []

  
