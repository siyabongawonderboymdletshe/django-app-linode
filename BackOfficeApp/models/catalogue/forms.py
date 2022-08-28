from django import forms
from BackOfficeApp.models.catalogue.models import *

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