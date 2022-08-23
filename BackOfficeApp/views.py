from django.shortcuts import render
from .models import ProductRequest, AccountItem, ProductItemImage, ProductItemImageForm, AccountItemForm, CustomerAsset, Account, Customer, CustomerRegistrationForm, AccountRegistrationForm, DashboardSession, DashboardSession, ProductCategoryForm, ProductItemForm
from django.http import HttpResponse
from django.db.models import F
import hashlib
import json

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
            customer = Customer.objects.filter(id_number = id)
            if not customer:
                customer= customerRegistrationForm.save()
                account = accountRegistrationForm.save(commit=False)
                account.customer = customer
                account.save()
              
                dashboard_session_context.add_customer_message  = 'The customer was successfully added!'
                dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_success'
                dashboard_session_context.add_customer_message_action_hyperlink_text = 'here.'
                dashboard_session_context.add_customer_message_action = 'You can now add the customer product item'
                dashboard_session_context.add_customer_message_action_hyperlink_url = f"BackOfficeApp:addproduct"
                dashboard_session_context.add_customer_message_action_hyperlink_url_query_string = f'account_id={account.id}&number_of_products={account.number_of_products}'
            else:
                dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_error'
                dashboard_session_context.add_customer_message  = 'An account with the same ID number already exists. Choose a different one.'
                dashboard_session_context.add_customer_message_action = 'You can update the customer information '
                dashboard_session_context.add_customer_message_action_hyperlink_text = 'here.'
                dashboard_session_context.add_customer_message_action_hyperlink_url = f"BackOfficeApp:updatecustomer"
                dashboard_session_context.add_customer_message_action_hyperlink_url_parameters = id
           
    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})

def update_customer_product(request, account_id):
    print(account_id)
    return HttpResponse(account_id)

def is_a_duplicate_request(request, account_id):
    form_data_string = f'{str(request.POST)}{str(request.FILES)}'
    hash_object = hashlib.sha256(json.dumps(form_data_string).encode())
   
    account = ProductRequest.objects.filter(account_id=account_id) 
    if not account:
        product_request = ProductRequest(account_id = account_id, hash_value = hash_object.hexdigest())
        product_request.save()
        return False
    return True

def get_products_forms(request, number_of_products, is_post_form = False):

    add_product_forms_list = []
    i = 1
    while i <= number_of_products:
        if request.POST and is_post_form:
            productItemForm = ProductItemForm(request.POST, use_required_attribute=False, prefix = f'productItemForm{i}')
            accountItemForm = AccountItemForm(request.POST, use_required_attribute=False, prefix = f'accountItemForm{i}')
            productItemImageForm = ProductItemImageForm(request.POST, request.FILES, use_required_attribute=False, prefix = f'productItemImageForm{i}') 
        else:
            productItemForm = ProductItemForm(use_required_attribute=False, prefix = f'productItemForm{i}')
            accountItemForm = AccountItemForm(use_required_attribute=False, prefix = f'accountItemForm{i}')
            productItemImageForm = ProductItemImageForm(use_required_attribute=False, prefix = f'productItemImageForm{i}')
        
        list = {
        'productItemForm': productItemForm,
        'accountItemForm': accountItemForm,
        'productItemImageForm': productItemImageForm,
        }
        add_product_forms_list.append(list)
        i += 1

    return add_product_forms_list

def add_customer_product(request):
    dashboard_session_context = DashboardSession()
    account_id = int(request.GET.get('account_id', -1))
    number_of_products = int(request.GET.get('number_of_products', -1))
    dashboard_session_context.add_customer_post_form_parameters = f'account_id={account_id}&number_of_products={number_of_products}'
    dashboard_session_context.display_template = 'AdminDashboard/dashboard_customer_add_product_item.html'
    
    dashboard_session_context.add_product_forms_list = get_products_forms(request, number_of_products)
    
    if is_a_duplicate_request(request, account_id):
        dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_error'
        dashboard_session_context.add_customer_message  = f'Oops! You have already added the same product(s) for the customer with account Id({account_id}) '
        dashboard_session_context.add_customer_message_action = 'You can update the details '
        dashboard_session_context.add_customer_message_action_hyperlink_text = 'here'
        dashboard_session_context.add_customer_message_action_hyperlink_url = f"BackOfficeApp:updateproduct"
        dashboard_session_context.add_customer_message_action_hyperlink_url_parameters = account_id
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
    
    if request.POST:
        dashboard_session_context.add_product_forms_list = get_products_forms(request, number_of_products, True)
        all_forms_are_valid = True
        for form in dashboard_session_context.add_product_forms_list:
            if not form['productItemForm'].is_valid() or not form['accountItemForm'].is_valid() or not form['productItemImageForm'].is_valid():
                all_forms_are_valid = False
                break

        if all_forms_are_valid:
            account = Account.objects.select_related('customer').get(id = account_id)
            customer = account.customer
           
            if not customer:
                dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_error'
                dashboard_session_context.add_customer_message  = 'A customer with the provided ID number does not exist.'
                dashboard_session_context.add_customer_message_action = 'You can add a new customer '
                dashboard_session_context.add_customer_message_action_hyperlink_text = 'here.'
                dashboard_session_context.add_customer_message_action_hyperlink_url = f"BackOfficeApp:addcustomer"
            else:
                count = 1
                for form in dashboard_session_context.add_product_forms_list:
                    
                    product_item = form['productItemForm'].save()
                    customer_asset = CustomerAsset(customer = customer, product_item = product_item)
                    customer_asset.save()
                    
                    account_item = AccountItem(account  = account, market_value = request.POST[f'accountItemForm{count}-market_value'], created_at = account.created_at, 
                                                product_item = product_item, operative_date = request.POST[f'accountItemForm{count}-operative_date'], updated_at =account.created_at)
                    account_item.save()

                    image = form['productItemImageForm'].save(commit=False)
                    image.product_item = product_item
                    image.save()

                dashboard_session_context.add_customer_message  = 'The customer product was successfully added!'
                dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_success'
                dashboard_session_context.add_customer_message_action_hyperlink_url_parameters = account_id
                dashboard_session_context.add_product_forms_list = dashboard_session_context.add_product_forms_list = get_products_forms(request, number_of_products)
                
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