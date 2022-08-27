from django import forms
from BackOfficeApp.models.product.models import *


class ProductItemForm(forms.ModelForm):
  class Meta:
    model = ProductItem
    fields = "__all__"
    labels = {
       'name' : '','serial_number' : '','year' : '','description' : '','category' : '', 'market_value':''
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
            'market_value': forms.NumberInput(
                attrs={'placeholder': 'Enter Market Value Here' }),
            
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
            },
            'market_value': {
                'required':'The Market Value is required.'
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
                attrs={'placeholder': 'Select Product Image Here', 'class':'custom-file-input'} ),
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
    widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Enter Name Here' }),
        }
    error_messages = {
            'name': {
                'required':'The Name is required.'
            }
    }   

class KeepProductImageForm(forms.ModelForm):
    class Meta:
        model = KeepProductImage
        fields = "__all__" 
        