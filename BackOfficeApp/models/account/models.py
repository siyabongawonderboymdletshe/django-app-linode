from django.db import models
from django.utils import timezone
from BackOfficeApp.models.customer.models import * 

class Account(models.Model):
  loan_amount = models.DecimalField("Loan Amount", max_digits=13, decimal_places=2, blank= False)
  rate = models.DecimalField("Rate", max_digits=5, decimal_places=2, blank= False)
  created_at = models.DateTimeField("Created Date", auto_now_add=True)
  number_of_products = models.IntegerField("Number Of Products", blank= False)
  payment_due_date = models.DateField("Payment Due Date", blank= False)
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.created_at = self.created_at
        return super(Account, self).save(*args, **kwargs)
  
  class Meta:
        ordering = ['created_at']

  def __str__(self):
    return f'{self.id}'
  
class AccountItem(models.Model):
  STATUS_CHOICES = (  ('AVAILABLE', 'AVAILABLE'),  ('SOLD', 'SOLD'), ('REMOVED', 'REMOVED'),  ('UNAVAILABLE', 'UNAVAILABLE'))
  account = models.ForeignKey(Account, on_delete=models.CASCADE)
  product_item = models.ManyToManyField(ProductItem, blank=False)
  status = models.CharField(max_length=255, choices= STATUS_CHOICES, default='AVAILABLE')
  created_at = models.DateTimeField("Created Date", blank= False)
  updated_at = models.DateTimeField("Updated Date")
  def __str__(self):
    return f'{self.account}'

  def save(self, *args, **kwargs):
        if self.id:
            self.updated_at = timezone.now()
        return super(AccountItem, self).save(*args, **kwargs)
