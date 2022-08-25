from django.urls import path
from .views import get_product_categories, add_product_category, get_customers_list, add_customer, update_customer, delete_customer, add_customer_product, update_customer_product


app_name = 'BackOfficeApp'

urlpatterns = [
   
    path('customers', view = get_customers_list, name='customers'),
    path('addcustomer', view=add_customer, name='addcustomer'),
    path('addproduct/', view=add_customer_product, name='addproduct'),
    path('addcategory/', view=add_product_category, name='add_product_category'),
    path('productcategories', view = get_product_categories, name='product_categories'),
    path('updatecustomer/<int:id_number>', view=update_customer, name='updatecustomer'),
    path('updatecustomer/delete/<int:id_number>', view=delete_customer, name='deletecustomer'),
    path('updateproduct/<int:account_id>', view=update_customer_product, name='updateproduct')


]
