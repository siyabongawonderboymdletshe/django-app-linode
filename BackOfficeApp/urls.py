from django.urls import path
from .views import get_accounts, delete_customer_account, get_customer_accounts, add_customer_product, update_customer_account, get_account_product, delete_customer_product, update_customer_product, get_all_customers_products, update_product_category, delete_product_category, get_product_categories, add_product_category, get_customers, add_customer, update_customer_personal_details, delete_customer, add_account_product, update_account_product


app_name = 'BackOfficeApp'

urlpatterns = [
   
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
    

]
