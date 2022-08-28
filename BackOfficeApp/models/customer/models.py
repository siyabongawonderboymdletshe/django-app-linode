from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from BackOfficeApp.models.product.models import *


class Customer(models.Model):
  GENDER_CHOICES = (  ('MALE', 'MALE'),  ('FEMALE', 'FEMALE'))
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


  
class CustomerAsset(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.customer} owns {self.product_item}'
