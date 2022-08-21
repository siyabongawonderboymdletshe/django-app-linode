from django.contrib import admin
from .models import Customer, Account, AccountItem, Catalogue, CustomerAsset, ProductCategory, ProductItem

class Customerdmin(admin.ModelAdmin):
    model: Customer
    actions = ['generate_client_report']
    list_display = ("id","first_name", "last_name", "email", "id_number", "home_address", "gender")
    list_filter = ("first_name", "last_name", "email", "id_number", "home_address", "gender")

class Accountdmin(admin.ModelAdmin):
    model: Account
    list_display = ("id","loan_amount", "rate", "customer", "created_at")
    list_filter = ("created_at", "rate")

# Register your models here.
admin.site.register(Customer, Customerdmin)
admin.site.register(Account, Accountdmin)
admin.site.register(AccountItem)
admin.site.register(Catalogue)
admin.site.register(CustomerAsset)
admin.site.register(ProductCategory)
admin.site.register(ProductItem)
