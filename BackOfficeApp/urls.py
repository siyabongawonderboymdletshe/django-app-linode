from django.urls import path
from BackOfficeApp.views.customer.views import *
from BackOfficeApp.views.account.views import *
from BackOfficeApp.views.product.views import *
from BackOfficeApp.views.category.views import *

app_name = 'BackOfficeApp'

urlpatterns = [
   
    #Customers
    path('allcustomers', view=get_all_customers, name='get_all_customers'), 
    path('addcustomer', view=add_customer, name='add_customer'),
    path('updatecustomer/<int:id_number>', view=update_customer_personal_details, name='update_customer_personal_details'),
    path('deletecustomer/<int:id_number>', view=delete_customer, name='delete_customer'),



    #Accounts
    path('accounts', view=get_all_accounts, name='get_all_accounts'),
    path('updatecustomeraccount/<int:account_id>', view=update_customer_account, name='update_customer_account'),
    path('accountproduct/<int:account_id>', view=get_account_product, name='get_account_product'),
    path('deletecustomeraccount/<int:account_id>', view=delete_customer_account, name='delete_customer_account'),
    path('customeraccounts/<int:id_number>', view=get_customer_accounts, name='get_customer_accounts'),
    path('addaccountproduct/', view=add_account_product, name='add_account_product'),
    path('addcustomeraccount', view=add_customer_account, name='add_customer_account'),
    #path('addcustomeraccount/<int:id_number>', view=add_customer_account, name='add_customer_account'),
    

    #Assets
    path('updatecustomerproduct/<int:product_id>', view=update_customer_product, name='update_customer_product'),
    path('deletecustomerproduct/<int:product_id>', view=delete_customer_product, name='delete_customer_product'),
    path('customerproducts', view = get_all_customers_products, name='get_all_customers_products'),
    path('addcustomerproduct', view=add_customer_product, name='add_customer_product'),


    #Categories
    path('productcategories', view = get_product_categories, name='get_product_categories'),
    path('deletecategory/<int:category_id>', view=delete_product_category, name='delete_product_category'),
    path('updatecategory/<int:category_id>', view=update_product_category, name='update_product_category'),
    path('addcategory/', view=add_product_category, name='add_product_category'),
]


"""
    path('customers', view = get_customers, name='get_customers'),
    path('addcustomer', view=add_customer, name='add_customer'),
    path('updatecustomer/<int:id_number>', view=update_customer_personal_details, name='update_customer_personal_details'),
    path('deletecustomer/<int:id_number>', view=delete_customer, name='delete_customer'),

    path('addaccountproduct/', view=add_account_product, name='add_account_product'),
    path('addcategory/', view=add_product_category, name='add_product_category'),

    
    path('addcustomerproduct', view=add_customer_product, name='add_customer_product'),
    path('customerproducts', view = get_all_customers_products, name='get_all_customers_products'),
    path('updatecustomerproduct/<int:product_id>', view=update_customer_product, name='update_customer_product'),
    path('deletecustomerproduct/<int:product_id>', view=delete_customer_product, name='delete_customer_product'),

    path('productcategories', view = get_product_categories, name='get_product_categories'),
    path('deletecategory/<int:category_id>', view=delete_product_category, name='delete_product_category'),
    path('updatecategory/<int:category_id>', view=update_product_category, name='update_product_category'),
    
   
    path('updateaccountproduct/<int:account_id>', view=update_account_product, name='update_account_product'),


    path('customeraccounts/<int:id_number>', view=get_customer_accounts, name='get_customer_accounts'),
    path('updatecustomeraccount/<int:account_id>', view=update_customer_account, name='update_customer_account'),


    path('accountproduct/<int:account_id>', view=get_account_product, name='get_account_product'),
    path('deletecustomeraccount/<int:account_id>', view=delete_customer_account, name='delete_customer_account'),
    path('accounts', view=get_accounts, name='get_accounts'),
    path('addcustomeraccount/<int:id_number>', view=add_customer_account, name='add_customer_account'),
    
   """
