from django.db import models
from django.contrib.auth.models import User

from django import forms

# Create your models here.

class ItemBuyer(models.Model):
  items = models.ManyToManyField('Item', blank=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE, default='')

  class Meta:
        ordering = ['user']

  def __str__(self):
    item_name = ''
    for i, item in enumerate(self.items.all()):
      item_name += f' {i+1}. [{item.name}]'
    return f'{self.user} has bought {item_name}'
      
  
class Item(models.Model):
  STATUS_CHOICES = (  ('AVAILABLE', 'AVAILABLE'),  ('SOLD', 'SOLD'), ('REMOVED', 'REMOVED'),  ('UNAVAILABLE', 'UNAVAILABLE'))
  name = models.CharField(max_length=255)
  description = models.CharField(max_length=255)
  amount = models.BigIntegerField()
  status = models.CharField(max_length=255, choices= STATUS_CHOICES, default='AVAILABLE')

  class Meta:
        ordering = ['status']

  def __str__(self):
    return f'{self.name}'


class RegistrationForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=100, min_length=2,
                            widget=forms.TextInput(attrs={'placeholder': 'User Name',
                                                          'class': 'form-control'}),
                             error_messages={'required':'User name is required.'})
    firstname = forms.CharField(label='First Name', max_length=100, min_length=2,
                                widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                            'class': 'form-control'}),
                                error_messages={'required':'First name is required. '})
    lastname = forms.CharField(label='Last Name', max_length=100, min_length=2,
                              widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                            'class': 'form-control'}),
                             error_messages={'required':'Last name is required.'})
    email = forms.EmailField(label='Email', max_length=100, min_length=2,
                            widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                          'class': 'form-control'}),
                            error_messages={'required':'Email is required.'})

    password = forms.CharField(max_length=64, min_length=2,
                              label="Password",
                              widget=forms.PasswordInput(attrs={'placeholder':
                                                                'Password',
                                                                'autocomplete': 'off',
                                                                'class': 'form-control'}),
                              error_messages={'required':'Password is required.'})


class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=100, min_length=2,
                            widget=forms.TextInput(attrs={'placeholder': 'User Name',
                                                          'class': 'form-control'}),
                             error_messages={'required':'User name is required.'})

    password = forms.CharField(max_length=64, min_length=2,
                              label="Password",
                              widget=forms.PasswordInput(attrs={'placeholder':
                                                                'Password',
                                                                'autocomplete': 'off',
                                                                'class': 'form-control'}),
                              error_messages={'required':'Password is required.'})

    