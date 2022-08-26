from django.shortcuts import render
from BackOfficeApp.models import Account, Customer
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from datetime import datetime, timedelta, date


def filter_customers(filter):

    if filter == 'today':
        return Account.objects.annotate(first_name=F('customer__first_name'), last_name=F('customer__last_name'), id_number=F('customer__id_number'), gender=F('customer__gender'), home_address=F('customer__home_address'), cell_phone_number=F('customer__cell_phone_number'), email=F('customer__email'), account_id=F('id')).filter(created_at__day = datetime.now().day)
    elif filter == 'yesterday':
        date = datetime.now() - timedelta(days = 1)
    elif filter == '5':
        date = datetime.now() - timedelta(days = 5)
    elif filter == '10':
        date = datetime.now() - timedelta(days = 10)
    elif filter == '15':
       date = datetime.now() - timedelta(days = 15)
    elif filter == '20':
       date = datetime.now() - timedelta(days = 20)
    elif filter == '25':
        date = datetime.now() - timedelta(days = 25)
    elif filter == '30':
       date = datetime.now() - timedelta(days = 30)
    elif filter == '>30':
       date = datetime.now() - timedelta(days = 31)
       return Account.objects.annotate(first_name=F('customer__first_name'), last_name=F('customer__last_name'), id_number=F('customer__id_number'), gender=F('customer__gender'), home_address=F('customer__home_address'), cell_phone_number=F('customer__cell_phone_number'), email=F('customer__email'), account_id=F('id')).filter(created_at__lt = date)
        
    return Account.objects.annotate(first_name=F('customer__first_name'), last_name=F('customer__last_name'), id_number=F('customer__id_number'), gender=F('customer__gender'), home_address=F('customer__home_address'), cell_phone_number=F('customer__cell_phone_number'), email=F('customer__email'), account_id=F('id')).filter(created_at__gte = date)

def admin_dashboard(request):
   
    customers = filter_customers(request.GET.get('filter', '30')).values()
    number_of_sales= len(Account.objects.values())
    number_of_customers= len(Customer.objects.values())

    temp_customers = []
    customers_list = []

    for c in customers:
        if c['customer_id'] not in temp_customers:
            temp_customers.append(c['customer_id'])
            customers_list.append(c)


    dashboard_session = {
        'display_template' : 'AdminDashboard/dashboard_landing_page.html',
        'customers' : customers_list,
        'sales': customers,
        'number_of_customers': number_of_customers,
        'number_of_sales': number_of_sales,
        'filtered_result': True
    }
    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session})