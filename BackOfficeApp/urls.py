from django.urls import path
from .views import get_customers_list, add_customer, update_customer, delete_customer


app_name = 'BackOfficeApp'

urlpatterns = [
   
    path('customers', view = get_customers_list, name='customers'),
    path('addcustomer', view=add_customer, name='addcustomer'),
    path('updatecustomer/<int:id_number>', view=update_customer, name='updatecustomer'),
    path('updatecustomer/delete/<int:id_number>', view=delete_customer, name='deletecustomer'),

]
