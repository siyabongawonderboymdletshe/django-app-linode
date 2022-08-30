from django.shortcuts import render
from BackOfficeApp.models.account.models import Account
from BackOfficeApp.models.customer.models import Customer
from BackOfficeApp.utils.customers.customer import *
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from datetime import datetime, timedelta, date
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required
from AdminDashboard.models.login.models import * 
from AdminDashboard.models.registration.models import * 
from django.contrib.auth import authenticate, login
from django.urls import reverse


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




def get_chart_data(data = ''):
        
    monthly_sales = [0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0, 0]
    list  = []

    #items = AccountItem.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(total=sum('account__loan_amount')).values('month', 'total') 
    items = Account.objects.filter().values('created_at__month').order_by('created_at__month').annotate(sum=Sum('loan_amount'))
    
    for i in items:
     #monthly_sales[(i['month'].month)-1] = i['total']
     monthly_sales[i['created_at__month']-1] = float(i['sum'])
     
        
    return monthly_sales 


def user_registration(request):
    dashboard_session_context = DashboardSession()
    if request.POST:
        regForm = RegistrationForm(request.POST, use_required_attribute=False)
        dashboard_session_context.add_login_form = regForm
        if not regForm.is_valid():
            return render (request, 'AdminDashboard/landing_page/registration/registration.html', {'dashboard_session': dashboard_session_context})
        regForm.save()
        return HttpResponseRedirect(reverse('AdminDashboard:login'))
        
    regForm = RegistrationForm(use_required_attribute=False)
    dashboard_session_context.add_login_form = regForm
    dashboard_session_context.url_query_string = request.GET.get('next', 'login')
    

    return render (request, 'AdminDashboard/landing_page/registration/registration.html', {'dashboard_session': dashboard_session_context})


def user_login(request):
    dashboard_session_context = DashboardSession()
    if request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return HttpResponse('USER DOES NOT EXIST!')
        login(request, user)
        return HttpResponseRedirect(request.GET.get('next', '/')) 
        
    loginForm = LoginForm(use_required_attribute=False)
    dashboard_session_context.add_login_form = loginForm
    dashboard_session_context.url_query_string = request.GET.get('next', '/')
    

    return render (request, 'AdminDashboard/landing_page/login/login.html', {'dashboard_session': dashboard_session_context})


@staff_member_required(redirect_field_name='next', login_url='AdminDashboard:login')
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
        'display_template' : 'AdminDashboard/landing_page/content.html',
        'customers' : customers_list,
        'sales': customers,
        'number_of_customers': number_of_customers,
        'number_of_sales': number_of_sales,
        'filtered_result': True,
        'chart_data': get_chart_data()
    }
    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session})