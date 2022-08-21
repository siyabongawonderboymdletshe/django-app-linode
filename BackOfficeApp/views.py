from django.shortcuts import render
from .models import Account, Customer, CustomerRegistrationForm, AccountRegistrationForm, DashboardSession, DashboardSession
from django.http import HttpResponse
from django.db.models import F


def get_customers_list(request):

    filter = request.GET.get('filter', 'active')
    if filter == 'all':
        customers = customers = Customer.objects.annotate(loan_amount=F('account__loan_amount'), rate=F('account__rate'), created_at=F('account__created_at'), account_id=F('account__id')).values()
    else:

        customers = Account.objects.annotate(first_name=F('customer__first_name'), last_name=F('customer__last_name'), id_number=F('customer__id_number'), gender=F('customer__gender'), home_address=F('customer__home_address'), cell_phone_number=F('customer__cell_phone_number'), email=F('customer__email'), account_id=F('id')).values()
        
    dashboard_session = {
        'display_template' : 'AdminDashboard/dashboard_customer_landing_page.html',
        'customers': customers,
    }
    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session})


def add_customer(request):  
    
    customerRegistrationForm = CustomerRegistrationForm(use_required_attribute=False)
    accountRegistrationForm = AccountRegistrationForm(use_required_attribute=False)
    
    dashboard_session_context = DashboardSession()
    dashboard_session_context.display_template = 'AdminDashboard/dashboard_customer_registration.html'
    dashboard_session_context.add_customer_form = customerRegistrationForm
    dashboard_session_context.add_account_form = accountRegistrationForm
    dashboard_session_context.add_customer_title  = 'Customer Registration'
    
    if request.POST:
        customerRegistrationForm = CustomerRegistrationForm(request.POST, use_required_attribute=False)
        accountRegistrationForm = AccountRegistrationForm(request.POST, use_required_attribute=False)
        dashboard_session_context.add_customer_form = customerRegistrationForm
        dashboard_session_context.add_account_form = accountRegistrationForm
        
        if customerRegistrationForm.is_valid() and accountRegistrationForm.is_valid():
            id = request.POST['id_number']
            customer = Customer.objects.filter(id_number = id).filter()
            if not customer:
                customer= customerRegistrationForm.save()
                print(customer)
                account = accountRegistrationForm.save(commit=False)
                account.customer = customer
                account.save()
                dashboard_session_context.add_customer_message  = 'The customer was successfully added!'
                dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_success'
            else:
                dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_error'
                dashboard_session_context.add_customer_message  = 'An account with the same ID number already exists. Choose a different one.'
                dashboard_session_context.add_customer_message_action = 'You can update the customer information '
                dashboard_session_context.add_customer_message_action_hyperlink_text = 'here.'
                dashboard_session_context.add_customer_message_action_hyperlink_url = f"BackOfficeApp:updatecustomer"
                dashboard_session_context.add_customer_message_action_hyperlink_url_parameters = id
           
    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})


def update_customer(request, id_number):
    try:
    
        dashboard_session_context = DashboardSession()
        dashboard_session_context.display_template = 'AdminDashboard/dashboard_update_customer.html'
        dashboard_session_context.add_customer_title  = 'Update Customer'
        accountRegistrationForm = AccountRegistrationForm(use_required_attribute=False)
        customerRegistrationForm = CustomerRegistrationForm(use_required_attribute=False)
        dashboard_session_context.add_customer_post_form_parameters = id_number
        
        if request.POST:
            customerRegistrationForm = CustomerRegistrationForm(request.POST, use_required_attribute=False)
            accountRegistrationForm = AccountRegistrationForm(request.POST, use_required_attribute=False)
            
            if customerRegistrationForm.is_valid() and accountRegistrationForm.is_valid():
        
                #check if the new id already exists
                id = request.POST['id_number']
                customer = Customer.objects.filter(id_number = id).first()
            
                if customer and id == id_number:
                    dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_error'
                    dashboard_session_context.add_customer_message  = 'An account with the same ID number already exists. Choose a different one.'
                    dashboard_session_context.add_customer_message_action = 'You can update the customer information '
                    dashboard_session_context.add_customer_message_action_hyperlink_text = 'here.'
                    dashboard_session_context.add_customer_message_action_hyperlink_url = f"BackOfficeApp:updatecustomer"
                    dashboard_session_context.add_customer_message_action_hyperlink_url_parameters = id
                    dashboard_session_context.add_customer_form = customerRegistrationForm
                    dashboard_session_context.add_account_form = accountRegistrationForm 
                    dashboard_session_context.add_customer_post_form_parameters = id  
                    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})

                else:
                    customer= customerRegistrationForm.save(commit=False)
                    
                    existing_customer = Customer.objects.filter(id_number = id_number).first()
                    existing_customer.first_name = customer.first_name
                    existing_customer.last_name = customer.last_name
                    existing_customer.email = customer.email
                    existing_customer.id_number = customer.id_number
                    existing_customer.cell_phone_number = customer.cell_phone_number
                    existing_customer.home_address = customer.home_address
                    existing_customer.gender = customer.gender
                    existing_customer.save()
                    
                    existing_account = Account.objects.select_related('customer').filter(customer__id_number__exact=id_number).first()
                    
                    account = accountRegistrationForm.save(commit=False)
                    existing_account.customer = existing_customer
                    existing_account.loan_amount = account.loan_amount
                    existing_account.rate = account.rate
                    existing_account.save()

                    dashboard_session_context.add_customer_form = customerRegistrationForm
                    dashboard_session_context.add_account_form = accountRegistrationForm 
                    dashboard_session_context.add_customer_message  = 'The customer details were successfully updated!'
                    dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_success'
                    
                    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
        
        account = Account.objects.select_related('customer').filter(customer__id_number__exact=id_number).first()
       
        if not account:
            dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_error'
            dashboard_session_context.add_customer_message  = 'The account you provided does not exist.'
            dashboard_session_context.add_customer_message_action = 'You can add a new customer '
            dashboard_session_context.add_customer_message_action_hyperlink_text = 'here.'
            dashboard_session_context.add_customer_message_action_hyperlink_url = f"BackOfficeApp:addcustomer"
            dashboard_session_context.add_customer_form = customerRegistrationForm
            dashboard_session_context.add_account_form = accountRegistrationForm   
            return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})

        accountRegistrationForm = AccountRegistrationForm(account.__dict__)
        customerRegistrationForm = CustomerRegistrationForm(account.customer.__dict__)

        dashboard_session_context.add_customer_form = customerRegistrationForm
        dashboard_session_context.add_account_form = accountRegistrationForm
              
        if not customerRegistrationForm.is_valid() and not accountRegistrationForm.is_valid():
            dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_error'
            dashboard_session_context.add_customer_message  = 'Oops! There was an issue with your request.'
            dashboard_session_context.add_customer_message_action = 'You can try again later or click '
            dashboard_session_context.add_customer_message_action_hyperlink_text = 'here.'
            dashboard_session_context.add_customer_message_action_hyperlink_url_parameters = id_number

        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
        
    except Exception as e:
        print(e)
        dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_error'
        dashboard_session_context.add_customer_message  = 'Oops! There was an issue with your request.'
        dashboard_session_context.add_customer_message_action = 'You can try again later or click '
        dashboard_session_context.add_customer_message_action_hyperlink_text = 'here.'
        dashboard_session_context.add_customer_message_action_hyperlink_url = f"BackOfficeApp:updatecustomer"
        dashboard_session_context.add_customer_message_action_hyperlink_url_parameters = id_number
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})


def delete_customer(request, id_number):
    try:
        dashboard_session_context = DashboardSession()
        customerRegistrationForm = CustomerRegistrationForm(use_required_attribute=False)
        accountRegistrationForm = AccountRegistrationForm(use_required_attribute=False)
        dashboard_session_context.add_customer_post_form_parameters = id_number
        dashboard_session_context.display_template = 'AdminDashboard/dashboard_update_customer.html'
        dashboard_session_context.add_customer_form = customerRegistrationForm
        dashboard_session_context.add_account_form = accountRegistrationForm   

        account = Account.objects.select_related('customer').filter(customer__id_number__exact=id_number).first()
        
        if not account:
            dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_error'
            dashboard_session_context.add_customer_message  = 'Oops! The customer you provided does not exist.'
            return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})

        account.delete()
        dashboard_session_context.add_customer_message  = 'The customer was successfully deleted!'
        dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_success'
        
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
    except Exception as e:
        print(e)