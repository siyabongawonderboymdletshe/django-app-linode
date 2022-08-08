from django.contrib import admin
from .models import Item, ItemBuyer, PaymentRequestData
# Register your models here.
admin.site.register(Item)
admin.site.register(ItemBuyer)
admin.site.register(PaymentRequestData)