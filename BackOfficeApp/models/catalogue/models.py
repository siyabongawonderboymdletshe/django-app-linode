from django.db import models
from BackOfficeApp.models.product.models import *

class Catalogue(models.Model):
  product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)

  def __str__(self):
    return f'{self.product_item} and ready for auction.'