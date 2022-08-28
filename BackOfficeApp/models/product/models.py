from django.db import models
import os

def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s_%s_%s.%s" % (instance.product_item.name, instance.product_item.year,'productItemId', instance.product_item.id, ext)
    return os.path.join('product_images', filename)


class ProductCategory(models.Model):
  name = models.CharField("Category", max_length=150, blank=False)
  def __str__(self):
    return f'{self.name}'

class ProductItem(models.Model):
  name = models.CharField("Name", max_length=150, blank=False)
  year = models.IntegerField("Year", blank= False)
  serial_number = models.CharField("Serial Number", max_length=150, blank=False)
  category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
  market_value = models.DecimalField("Market Value", max_digits=13, decimal_places=2, blank= False)
  description = models.TextField("Description", blank=False, default="")
  
  def __str__(self):
    return f'{self.id}, {self.year}, {self.name}, {self.serial_number}'

class ProductItemImage(models.Model):
  product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
  image = models.ImageField(upload_to=content_file_name)
  def __str__(self):
    return f'{os.path.basename(self.image.name)}'


class KeepProductImage(models.Model):
    keep_image = models.BooleanField()

class ProductRequest(models.Model):
  account_id = models.IntegerField("Account Id", blank= False)
  hash_value = models.CharField("Request Hash", max_length=255)
  created_at = models.DateTimeField("Created Date", blank= False, auto_now_add = True)
  
  def __str__(self):
    return f'Hash = [{self.hash_value}], Account = {self.account_id}'

class UpdateProductData:
    is_product_update=False
    product_item_list = ''
    product_item_image_list = ''

    
