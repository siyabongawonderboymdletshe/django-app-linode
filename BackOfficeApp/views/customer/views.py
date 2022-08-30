from django.shortcuts import render
from django.db.models import F
from BackOfficeApp.utils.customers.customer import get_dashboard_session_context
from BackOfficeApp.models.customer.models import *
from BackOfficeApp.models.customer.forms import *
from BackOfficeApp.models.account.models import *
from BackOfficeApp.models.account.forms import *
from BackOfficeApp.utils.customers.models import DashboardSession
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(redirect_field_name='next', login_url='AdminDashboard:login')
def get_all_customers(request):
    filter = request.GET.get('filter', 'all')
    if filter == 'all':
        customers = customers = Customer.objects.annotate(loan_amount=F('account__loan_amount'), rate=F('account__rate'), created_at=F('account__created_at'), account_id=F('account__id')).values()
    else:

        customers = Account.objects.annotate(first_name=F('customer__first_name'), last_name=F('customer__last_name'), id_number=F('customer__id_number'), gender=F('customer__gender'), home_address=F('customer__home_address'), cell_phone_number=F('customer__cell_phone_number'), email=F('customer__email'), account_id=F('id')).values()

    dashboard_session_context = get_dashboard_session_context(display_template='AdminDashboard/customer/show_all_customers.html')   
    dashboard_session_context.all_customers = customers
   
    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})

@staff_member_required(redirect_field_name='next', login_url='AdminDashboard:login')
def add_customer(request):  

    customerRegistrationForm = CustomerRegistrationForm(use_required_attribute=False)
    accountRegistrationForm = AccountRegistrationForm(use_required_attribute=False)
    
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/customer/add_customer.html',
    title='Add Customer', add_account_form = accountRegistrationForm, add_customer_form = customerRegistrationForm)

    if request.POST:
        customerRegistrationForm = CustomerRegistrationForm(request.POST, use_required_attribute=False)
        accountRegistrationForm = AccountRegistrationForm(request.POST, use_required_attribute=False)
        dashboard_session_context.add_customer_form = customerRegistrationForm
        dashboard_session_context.add_account_form = accountRegistrationForm
        
        if customerRegistrationForm.is_valid() and accountRegistrationForm.is_valid():
            id = request.POST['id_number']
            customer = Customer.objects.filter(id_number = id)
            if not customer:
                customer= customerRegistrationForm.save()
                account = accountRegistrationForm.save(commit=False)
                account.customer = customer
                account.save()
                
                dashboard_session_context = get_dashboard_session_context( display_template='AdminDashboard/customer/add_customer.html',
                message='The customer was successfully added!', message_class='add_customer_message_class_success', message_action='You can now add the customer asset', title='Customer Registration', hyperlink_text='here.', 
                hyperlink_url='BackOfficeApp:add_account_product', query_string=f'account_id={account.id}', add_account_form = accountRegistrationForm, add_customer_form = customerRegistrationForm, modal_close_url='BackOfficeApp:get_all_customers')
                
            else:
                dashboard_session_context = get_dashboard_session_context('AdminDashboard/customer/add_customer.html',
                message='An account with the same ID number already exists. Choose a different one.', message_class='add_customer_message_class_error', message_action='You can update the customer information ', title='Add Customer', hyperlink_text='here.', 
                hyperlink_url='BackOfficeApp:update_customer_personal_details', hyperlink_url_parameters=id, add_account_form = accountRegistrationForm, add_customer_form = customerRegistrationForm, modal_close_url='BackOfficeApp:get_all_customers')
                

    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})

@staff_member_required(redirect_field_name='next', login_url='AdminDashboard:login')
def update_customer_personal_details(request, id_number):
    #try:
        dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/customer/update_customer.html', hyperlink_url_parameters=id_number, hyperlink_url='BackOfficeApp:delete_customer')

        customerRegistrationForm = CustomerRegistrationForm(use_required_attribute=False)
        dashboard_session_context.add_customer_post_form_parameters = id_number
        dashboard_session_context.customer_id_number = id_number
        if request.POST:
        
            customerRegistrationForm = CustomerRegistrationForm(request.POST, use_required_attribute=False)
            dashboard_session_context.add_customer_form = customerRegistrationForm
           
            if customerRegistrationForm.is_valid():
                id = request.POST['id_number']
                customer = Customer.objects.filter(id_number = id).first()
                
                #check if the new id already exists
                if customer and id == id_number:
                    print('customer and id == id_number : ')
                    dashboard_session_context = get_dashboard_session_context(message='An account with the same ID number already exists. Choose a different one.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/customer/update_customer.html',
                    title='Update Customer', hyperlink_text='here', message_action = 'You can update the customer information ',  hyperlink_url='BackOfficeApp:update_customer', modal_close_url='BackOfficeApp:get_all_customers_products', hyperlink_url_parameters=id, 
                    post_form_parameters=id, add_customer_form=customerRegistrationForm)
                    
                    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
                else:
                    existing_customer = Customer.objects.filter(id_number = id_number).first()
                    existing_account = Account.objects.select_related('customer').filter(customer__id_number__exact=id_number).first()
                    customerRegistrationForm = CustomerRegistrationForm(request.POST, use_required_attribute=False, instance=existing_customer)
                
                    customerRegistrationForm.save()
                    
    
                    dashboard_session_context = get_dashboard_session_context( display_template='AdminDashboard/customer/update_customer.html',
                    message='The customer details were successfully updated', message_class='add_customer_message_class_success', message_action='You can view details ', title='Update Customer', hyperlink_text='here.', 
                    hyperlink_url='BackOfficeApp:update_customer_personal_details', add_customer_form = customerRegistrationForm, modal_close_url='BackOfficeApp:get_all_customers', hyperlink_url_parameters=id_number, post_form_parameters=id_number)
                    dashboard_session_context.customer_account_id = existing_account.id
                    dashboard_session_context.customer_id_number = id_number
                    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
            
            return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
        customer = Customer.objects.filter(id_number=id_number).first()
        if not customer:
            dashboard_session_context = get_dashboard_session_context( display_template='AdminDashboard/dashboard_update_customer_personal_details.html',
                    message='The customers you provided does not exist', message_class='add_customer_message_class_error', message_action='You can add a new customer  ', title='Update Customer', hyperlink_text='here.', 
                    hyperlink_url='BackOfficeApp:add_customer', add_customer_form = customerRegistrationForm, modal_close_url='BackOfficeApp:get_all_customers')
            dashboard_session_context.customer_id_number = id_number
            
            return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
        
    
        customerRegistrationForm = CustomerRegistrationForm(customer.__dict__, use_required_attribute=False)

        dashboard_session_context.add_customer_form = customerRegistrationForm

        return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
        
    #except Exception as e:
       # print(e)
       # return HttpResponse(e)
        """
        dashboard_session_context = get_dashboard_session_context( display_template='AdminDashboard/dashboard_add_customer_product.html',
                    message='Oops! There was an issue with your request.', message_class='add_customer_message_class_error', message_action='You can try again later or click ', title='Update Customer', hyperlink_text='here.', 
                    hyperlink_url='BackOfficeApp:add_customer', add_account_form = accountRegistrationForm, add_customer_form = customerRegistrationForm, modal_close_url='BackOfficeApp:get_customers', hyperlink_url_parameters = id_number)
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
         """

@staff_member_required(redirect_field_name='next', login_url='AdminDashboard:login')
def delete_customer(request, id_number):
    #try:
        dashboard_session_context = DashboardSession()
        customerRegistrationForm = CustomerRegistrationForm(use_required_attribute=False)
        accountRegistrationForm = AccountRegistrationForm(use_required_attribute=False)
        dashboard_session_context.add_customer_post_form_parameters = id_number
        dashboard_session_context.display_template = 'AdminDashboard/customer/update_customer.html'
        dashboard_session_context.add_customer_form = customerRegistrationForm
        dashboard_session_context.add_account_form = accountRegistrationForm
        dashboard_session_context.customer_id_number = id_number   

        customer = Customer.objects.filter(id_number=id_number).first()
    
        if not customer:
            dashboard_session_context = get_dashboard_session_context(message='Oops! The customer you provided does not exist.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/customer/update_customer.html',
                title='Delete Customer', add_customer_form = customerRegistrationForm, add_account_form = accountRegistrationForm, modal_close_url='BackOfficeApp:get_all_customers', post_form_parameters = id_number)
            dashboard_session_context.customer_id_number = id_number
            return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
        customer.delete()
        dashboard_session_context.add_customer_message  = 'The customer was successfully deleted!'
        dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_success'
        dashboard_session_context.modal_close_url = 'BackOfficeApp:get_all_customers'
        
        return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
    #except Exception as e:
       # print(e)

@staff_member_required(redirect_field_name='next', login_url='AdminDashboard:login')
def delete_customer_account(request, account_id):
    #try:
        dashboard_session_context = DashboardSession()
        customerRegistrationForm = CustomerRegistrationForm(use_required_attribute=False)
        accountRegistrationForm = AccountRegistrationForm(use_required_attribute=False)
        dashboard_session_context.add_customer_post_form_parameters = account_id
        dashboard_session_context.display_template = 'AdminDashboard/dashboard_update_customer_account_details.html'
        dashboard_session_context.add_customer_form = customerRegistrationForm
        dashboard_session_context.add_account_form = accountRegistrationForm
        dashboard_session_context.customer_account_id = account_id   

        account = Account.objects.filter(id=account_id).first()
        
        if not account:
            dashboard_session_context = get_dashboard_session_context(message='Oops! The account you provided does not exist.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_update_customer_account_detailsr.html',
                title='Delete Account', add_customer_form = customerRegistrationForm, add_account_form = accountRegistrationForm, modal_close_url='BackOfficeApp:get_customers', post_form_parameters = account_id)
            dashboard_session_context.customer_account_id = account_id 
            return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})

        account.delete()
        dashboard_session_context.add_customer_message  = 'The account was successfully deleted!'
        dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_success'
        
        return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
    #except Exception as e:
       # print(e)

