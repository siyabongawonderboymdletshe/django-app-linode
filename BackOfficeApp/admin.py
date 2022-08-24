from django.contrib import admin
from .models import ProductRequest, ProductItemImage, Customer, Account, AccountItem, Catalogue, CustomerAsset, ProductCategory, ProductItem

class Customerdmin(admin.ModelAdmin):
    model: Customer
    actions = ['generate_client_report']
    list_display = ("id","first_name", "last_name", "email", "id_number", "home_address", "gender")
    list_filter = ("first_name", "last_name", "email", "id_number", "home_address", "gender")

class Accountdmin(admin.ModelAdmin):
    model: Account
    list_display = ("id","loan_amount", "rate", "customer", "created_at")
    list_filter = ("created_at", "rate")

class ProductItemAdmin(admin.ModelAdmin):
    model: ProductItem
    list_display = ("id","name","year", "serial_number", "category", "description")
    list_filter = ("category", "year")

class CustomerAssetAdmin(admin.ModelAdmin):
    model: CustomerAsset
    list_display = ("id","customer","product_item")
    list_filter = ("customer", "product_item")

class ProductRequestAdmin(admin.ModelAdmin):
    model: ProductRequest
    list_display = ("id","account_id","hash_value", "created_at")
    list_filter = ("created_at","account_id")

class AccountItemAdmin(admin.ModelAdmin):
    model: AccountItem
    list_display = ("id","account", "status", "created_at","updated_at")
    filter_horizontal = ('product_item',)
    list_filter = ("created_at","account_id")

# Register your models here.
admin.site.register(Customer, Customerdmin)
admin.site.register(Account, Accountdmin)
admin.site.register(AccountItem, AccountItemAdmin)
admin.site.register(Catalogue)
admin.site.register(CustomerAsset, CustomerAssetAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductItem, ProductItemAdmin)
admin.site.register(ProductItemImage)
admin.site.register(ProductRequest, ProductRequestAdmin)