from django.shortcuts import render
from .models import ProductCategory, ProductItem, UpdateProductData, KeepProductImageForm, ProductRequest, AccountItem, ProductItemImage, ProductItemImageForm, CustomerAsset, Account, Customer, CustomerRegistrationForm, AccountRegistrationForm, DashboardSession, DashboardSession, ProductCategoryForm, ProductItemForm
from django.http import HttpResponse
from django.db.models import F
import hashlib
import json



def get_request_hash_value(request):
    form_data_string = f'{str(request.POST)}{str(request.FILES)}'
    hash_object = hashlib.sha256(json.dumps(form_data_string).encode())
    return hash_object.hexdigest()

def is_a_duplicate_request(request):
    account = ProductRequest.objects.filter(hash_value=get_request_hash_value(request))
    if not account:
        return False
    return True

def get_dashboard_session_context(display_template='', message='', message_class='', message_action='', title='', hyperlink_text='', hyperlink_url='', hyperlink_url_parameters='', post_form_parameters='', 
    query_string ='', modal_close_url = '', add_customer_form = '', add_account_form = '', add_product_forms_list=''):

    dashboard_session_context = DashboardSession()
    dashboard_session_context.add_customer_message_class  = message_class
    dashboard_session_context.add_customer_message  = message
    dashboard_session_context.add_customer_message_action = message_action
    dashboard_session_context.add_customer_message_action_hyperlink_text = hyperlink_text
    dashboard_session_context.add_customer_message_action_hyperlink_url = hyperlink_url
    dashboard_session_context.add_customer_message_action_hyperlink_url_parameters = hyperlink_url_parameters
    dashboard_session_context.add_customer_message_action_hyperlink_url_query_string = query_string
    dashboard_session_context.add_customer_post_form_parameters = post_form_parameters
    dashboard_session_context.display_template = display_template
    dashboard_session_context.add_customer_title = title
    dashboard_session_context.modal_close_url = modal_close_url
    dashboard_session_context.add_customer_form = add_customer_form
    dashboard_session_context.add_account_form = add_account_form
    dashboard_session_context.add_product_forms_list = add_product_forms_list
    
    return dashboard_session_context

def get_products_forms(request, number_of_products=1, is_post_form =False, update_product_data ='', use_prefix = True ):
    add_product_forms_list = []
    
    if update_product_data and update_product_data.is_product_update:
        i = 1
        for item in update_product_data.product_item_list:
            item_dictionary = item.__dict__
            item_dictionary['category'] = item.category
          
            new_dictionary = {}
            for k in item_dictionary:
                new_dictionary[f'productItemForm{i}-{k}'] = item_dictionary[k]
    
        
            image = ProductItemImage.objects.filter(product_item_id = item.id).first()
    
            productItemForm = ProductItemForm(new_dictionary, use_required_attribute=False, prefix = f'productItemForm{i}')
            productItemImageForm = ProductItemImageForm(use_required_attribute=False, prefix = f'productItemImageForm{i}')
            keepProductImage = KeepProductImageForm(use_required_attribute=False, prefix = f'updateProductImageForm{i}')
           
            list = {
            'productItemForm': productItemForm,
            'productItemImageForm': productItemImageForm,
            'keepProductImage': keepProductImage,
            'image':f'{image.image}'
            }
            add_product_forms_list.append(list)
            i += 1

        return add_product_forms_list

    i = 1
    while i <= number_of_products:     
        if request.POST and is_post_form:
            productItemForm = ProductItemForm(request.POST, use_required_attribute=False, prefix = f'productItemForm{i}' if use_prefix else '')
            productItemImageForm = ProductItemImageForm(request.POST, request.FILES, use_required_attribute=False, prefix = f'productItemImageForm{i}') 
            keepProductImage = KeepProductImageForm(request.POST, use_required_attribute=False, prefix = f'updateProductImageForm{i}') 
        else:
            productItemForm = ProductItemForm(use_required_attribute=False, prefix = f'productItemForm{i}')
            productItemImageForm = ProductItemImageForm(use_required_attribute=False, prefix = f'productItemImageForm{i}')
            keepProductImage = KeepProductImageForm(use_required_attribute=False, prefix = f'updateProductImageForm{i}') 
        
        list = {
        'productItemForm': productItemForm,
        'productItemImageForm': productItemImageForm,
        'keepProductImage': keepProductImage,
        }
        add_product_forms_list.append(list)
        i += 1
        
    return add_product_forms_list

def save_post_update_product_form(request, account_items):
    i = 1
    for item in account_items:
        print(item)
        image = ProductItemImage.objects.filter(product_item_id = item.id).first()

        productItemForm = ProductItemForm(request.POST, use_required_attribute=False, prefix = f'productItemForm{i}', instance=item)
        productItemImageForm = ProductItemImageForm(request.POST, request.FILES, use_required_attribute=False, prefix = f'productItemImageForm{i}', instance=image)
        
        print('productItemImageForm valid? ', productItemImageForm.is_valid(), request.FILES)
        
        productItemForm.save()
        productItemImageForm.save()
        i += 1



#Customer
def get_customers(request):

    filter = request.GET.get('filter', 'all')
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
    
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_customer_registration.html',
    title='Customer Registration', add_account_form = accountRegistrationForm, add_customer_form = customerRegistrationForm)

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
                
                dashboard_session_context = get_dashboard_session_context( display_template='AdminDashboard/dashboard_customer_registration.html',
                message='The customer was successfully added!', message_class='add_customer_message_class_success', message_action='You can now add the customer product item', title='Customer Registration', hyperlink_text='here.', 
                hyperlink_url='BackOfficeApp:add_account_product', query_string=f'account_id={account.id}', add_account_form = accountRegistrationForm, add_customer_form = customerRegistrationForm, modal_close_url='BackOfficeApp:get_customers')
                
            else:
                dashboard_session_context = get_dashboard_session_context('AdminDashboard/dashboard_customer_registration.html',
                message='An account with the same ID number already exists. Choose a different one.', message_class='add_customer_message_class_error', message_action='You can update the customer information ', title='Customer Registration', hyperlink_text='here.', 
                hyperlink_url='BackOfficeApp:update_customer_personal_details', hyperlink_url_parameters=id, add_account_form = accountRegistrationForm, add_customer_form = customerRegistrationForm, modal_close_url='BackOfficeApp:get_customers')
                

    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
def update_customer_personal_details(request, id_number):
    #try:
        dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_update_customer_personal_details.html', hyperlink_url_parameters=id_number, hyperlink_url='BackOfficeApp:delete_customer')

        customerRegistrationForm = CustomerRegistrationForm(use_required_attribute=False)
        dashboard_session_context.add_customer_post_form_parameters = id_number
        dashboard_session_context.customer_id_number = id_number
        if request.POST:
           
           #This is for removing unwanted date format, 2022-08-30 00:00:00
            payment_due_date = request.POST['payment_due_date']
            payment_due_date  = payment_due_date.replace(' 00:00:00','')
            _mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['payment_due_date'] = payment_due_date
            request.POST._mutable = _mutable

            customerRegistrationForm = CustomerRegistrationForm(request.POST, use_required_attribute=False)
            dashboard_session_context.add_customer_form = customerRegistrationForm
           

            if customerRegistrationForm.is_valid() and accountRegistrationForm.is_valid():
                id = request.POST['id_number']
                customer = Customer.objects.filter(id_number = id).first()
                
                #check if the new id already exists
                if customer and id == id_number:
                    print('customer and id == id_number : ')
                    dashboard_session_context = get_dashboard_session_context(message='An account with the same ID number already exists. Choose a different one.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_add_customer_product.html',
                    title='Update Customer', hyperlink_text='here', message_action = 'You can update the customer information ',  hyperlink_url='BackOfficeApp:update_customer', modal_close_url='BackOfficeApp:get_all_customers_products', hyperlink_url_parameters=id, 
                    post_form_parameters=id, add_customer_form=customerRegistrationForm, add_account_form=accountRegistrationForm)
                    
                    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})

                else:
                    existing_customer = Customer.objects.filter(id_number = id_number).first()
                    existing_account = Account.objects.select_related('customer').filter(customer__id_number__exact=id_number).first()
                    customerRegistrationForm = CustomerRegistrationForm(request.POST, use_required_attribute=False, instance=existing_customer)
                    accountRegistrationForm = AccountRegistrationForm(request.POST, use_required_attribute=False, instance=existing_account)
                    
                    customerRegistrationForm.save()
                    accountRegistrationForm.save()
                   
                    dashboard_session_context = get_dashboard_session_context( display_template='AdminDashboard/dashboard_update_customer.html',
                    message='The customer details were successfully updated', message_class='add_customer_message_class_success', message_action='You can view details ', title='Update Customer', hyperlink_text='here.', 
                    hyperlink_url='BackOfficeApp:update_customer', add_account_form = accountRegistrationForm, add_customer_form = customerRegistrationForm, modal_close_url='BackOfficeApp:get_customers', hyperlink_url_parameters=id_number, post_form_parameters=id_number)
                    dashboard_session_context.customer_account_id = existing_account.id
                    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
            
            return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
        customer = Customer.objects.filter(id_number=id_number).first()
        if not customer:
            dashboard_session_context = get_dashboard_session_context( display_template='AdminDashboard/dashboard_update_customer_personal_details.html',
                    message='The customers you provided does not exist', message_class='add_customer_message_class_error', message_action='You can add a new customer  ', title='Update Customer', hyperlink_text='here.', 
                    hyperlink_url='BackOfficeApp:add_customer', add_customer_form = customerRegistrationForm, modal_close_url='BackOfficeApp:get_customers')
            dashboard_session_context.customer_id_number = id_number
            return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
        
    
        customerRegistrationForm = CustomerRegistrationForm(customer.__dict__, use_required_attribute=False)

        dashboard_session_context.add_customer_form = customerRegistrationForm

        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
        
    #except Exception as e:
       # print(e)
       # return HttpResponse(e)
        """
        dashboard_session_context = get_dashboard_session_context( display_template='AdminDashboard/dashboard_add_customer_product.html',
                    message='Oops! There was an issue with your request.', message_class='add_customer_message_class_error', message_action='You can try again later or click ', title='Update Customer', hyperlink_text='here.', 
                    hyperlink_url='BackOfficeApp:add_customer', add_account_form = accountRegistrationForm, add_customer_form = customerRegistrationForm, modal_close_url='BackOfficeApp:get_customers', hyperlink_url_parameters = id_number)
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
         """

def delete_customer(request, id_number):
    #try:
        dashboard_session_context = DashboardSession()
        customerRegistrationForm = CustomerRegistrationForm(use_required_attribute=False)
        accountRegistrationForm = AccountRegistrationForm(use_required_attribute=False)
        dashboard_session_context.add_customer_post_form_parameters = id_number
        dashboard_session_context.display_template = 'AdminDashboard/dashboard_update_customer_personal_details.html'
        dashboard_session_context.add_customer_form = customerRegistrationForm
        dashboard_session_context.add_account_form = accountRegistrationForm
        dashboard_session_context.customer_id_number = id_number   

        customer = Customer.objects.filter(id_number=id_number).first()
    
        if not customer:
            dashboard_session_context = get_dashboard_session_context(message='Oops! The customer you provided does not exist.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_update_customer_personal_details.html',
                title='Delete Customer', add_customer_form = customerRegistrationForm, add_account_form = accountRegistrationForm, modal_close_url='BackOfficeApp:get_customers', post_form_parameters = id_number)
            dashboard_session_context.customer_id_number = id_number
            return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})

        customer.delete()
        dashboard_session_context.add_customer_message  = 'The customer was successfully deleted!'
        dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_success'
        dashboard_session_context.modal_close_url = 'BackOfficeApp:get_customers'
        
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
    #except Exception as e:
       # print(e)

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
                title='Delete Account', add_customer_form = customerRegistrationForm, add_account_form = accountRegistrationForm, modal_close_url='BackOfficeApp:get_customers', post_form_parameters = id_number)
            dashboard_session_context.customer_account_id = account_id 
            return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})

        account.delete()
        dashboard_session_context.add_customer_message  = 'The account was successfully deleted!'
        dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_success'
        
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
    #except Exception as e:
       # print(e)

#Account
def update_account_product(request, account_id):
    account_item = AccountItem.objects.filter(account__id__exact=account_id).first()
    number_of_products = 1 if not account_item  else account_item.account.number_of_products
    
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_customer_update_product_item.html',
    title='Add Customer Product', post_form_parameters = account_id)
    
    if not account_item:
        dashboard_session_context = get_dashboard_session_context(message=f'The account with Id {account_id} does not exist', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_customer_add_product_item.html',
            title='Add Customer Product', message_action='You can add a new customer ', hyperlink_text='here', hyperlink_url='BackOfficeApp:addcustomer', modal_close_url='BackOfficeApp:customers')
        dashboard_session_context.add_product_forms_list = get_products_forms(request, number_of_products)
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
    
    if request.POST:
        dashboard_session_context.add_product_forms_list = get_products_forms(request, number_of_products, is_post_form=True)
        all_forms_are_valid = True
        for form in dashboard_session_context.add_product_forms_list:
            if form['keepProductImage']:
                if not form['productItemImageForm'].is_valid() and not form['keepProductImage'].save(commit=False).keep_image:
                    all_forms_are_valid = False
                    break

            if not form['productItemForm'].is_valid():
                all_forms_are_valid = False
                break
        
        if all_forms_are_valid:
            account = Account.objects.select_related('customer').get(id = account_id)
            customer = account.customer
            if not customer:
                dashboard_session_context = get_dashboard_session_context(message='A customer with the provided ID number does not exist.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_customer_add_product_item.html',
                title='Update Customer Product', hyperlink_text='here', message_action = 'You can add a new customer',  hyperlink_url='BackOfficeApp:addcustomer', modal_close_url='BackOfficeApp:customers')
            else:
                save_post_update_product_form(request, account_item.product_item.all())
                dashboard_session_context = get_dashboard_session_context(message='The customer product was successfully updated!', message_class='add_customer_message_class_success',  display_template ='AdminDashboard/dashboard_customer_add_product_item.html',
                title='Update Customer Product', hyperlink_text='here', message_action = 'You can add a new customer',  hyperlink_url='BackOfficeApp:addcustomer', modal_close_url='BackOfficeApp:customers')
                
                dashboard_session_context.add_product_forms_list = get_products_forms(request, number_of_products)

        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})

    data = UpdateProductData()
    data.is_product_update = True
    data.product_item_list = account_item.product_item.all()
    dashboard_session_context.add_product_forms_list = get_products_forms(request, number_of_products if number_of_products > 0 else 1, update_product_data= data)
    
    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
def add_account_product(request):
    account_id = int(request.GET.get('account_id', -1))
    account = Account.objects.filter(id = account_id).first()
    number_of_products = 1 if not account  else account.number_of_products

    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_add_account_product.html',
    title='Add Customer Product', post_form_parameters = f'account_id={account_id}&number_of_products={number_of_products}')
   
    dashboard_session_context.add_product_forms_list = get_products_forms(request, number_of_products if number_of_products > 0 else 1)
    
    if not account:
        list =  dashboard_session_context.add_product_forms_list
        dashboard_session_context = get_dashboard_session_context(message=f'The account with Id {account_id} does not exist', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_add_account_product.html',
            title='Add Customer Product', message_action='You can add a new customer ', hyperlink_text='here', hyperlink_url='BackOfficeApp:addcustomer', modal_close_url='BackOfficeApp:customers')
        dashboard_session_context.add_product_forms_list = list
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
    
    if request.POST:
        if is_a_duplicate_request(request):
            list =  dashboard_session_context.add_product_forms_list
            dashboard_session_context = get_dashboard_session_context(message=f'Oops! You have already added the same product(s) for the customer with account Id({account_id}) ', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_add_account_product.html',
            title='Add Customer Product', message_action='You can update the customer product details', hyperlink_text='here', hyperlink_url='BackOfficeApp:get_account_product', hyperlink_url_parameters = account_id, modal_close_url='BackOfficeApp:get_customers')
            dashboard_session_context.add_product_forms_list = list
           
            return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
        
        dashboard_session_context.add_product_forms_list = get_products_forms(request, number_of_products, True)
        all_forms_are_valid = True
        for form in dashboard_session_context.add_product_forms_list:
            if not form['productItemForm'].is_valid()  or not form['productItemImageForm'].is_valid():
                all_forms_are_valid = False
                break

        if all_forms_are_valid:
            account = Account.objects.select_related('customer').get(id = account_id)
            customer = account.customer
           
            if not customer:
                dashboard_session_context = get_dashboard_session_context(message='A customer with the provided ID number does not exist.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_add_account_product.html',
                title='Add Customer Product', hyperlink_text='here', message_action = 'You can add a new customer',  hyperlink_url='BackOfficeApp:addcustomer', modal_close_url='BackOfficeApp:customers')
            else:
                account_item = AccountItem(account  = account, created_at = account.created_at, updated_at =account.created_at)
                account_item.save()
                for form in dashboard_session_context.add_product_forms_list:
                    
                    product_item = form['productItemForm'].save()
                    print()
                    customer_asset = CustomerAsset(customer = customer, product_item = product_item)
                    customer_asset.save()
                    
                    account_item.product_item.add(product_item)

                    image = form['productItemImageForm'].save(commit=False)
                    image.product_item = product_item
                    image.save()

                    product_request = ProductRequest(account_id = account_id, hash_value = get_request_hash_value(request))
                    product_request.save()

                account_item.save()
                
                dashboard_session_context = get_dashboard_session_context(message='The customer product was successfully added!', message_class='add_customer_message_class_success',  display_template ='AdminDashboard/dashboard_add_account_product.html',
                title='Add Customer Product', hyperlink_text='here', message_action = 'You can add a new customer',  hyperlink_url='BackOfficeApp:add_customer', modal_close_url='BackOfficeApp:get_customers')
                
                dashboard_session_context.add_product_forms_list = get_products_forms(request, number_of_products)
                
    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
def get_customer_accounts(request, id_number):
    customer = Customer.objects.filter(id_number=id_number).first()
    customerRegistrationForm = CustomerRegistrationForm(use_required_attribute=False)
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_customer_accounts_landing_page.html')
    dashboard_session_context.customer_id_number = id_number

    if not customer:
        dashboard_session_context = get_dashboard_session_context(message='Oops! The customer you provided does not exist.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_update_customer_personal_details.html',
                title='Customer Account', add_customer_form = customerRegistrationForm, modal_close_url='BackOfficeApp:get_customers', post_form_parameters = id_number)
        dashboard_session_context.customer_id_number = id_number
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})

    accounts = Account.objects.select_related('customer').filter(customer__id_number__exact=id_number)
    dashboard_session_context.all_customers_accounts = accounts

    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
def update_customer_account(request, account_id):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_update_customer_account_details.html', hyperlink_url_parameters=account_id, hyperlink_url='BackOfficeApp:delete_customer_account')
    
    dashboard_session_context.customer_account_id = account_id
    account = Account.objects.filter(id = account_id).first()
    accountRegistrationForm = AccountRegistrationForm(use_required_attribute=False)
    
    if not account:
        dashboard_session_context = get_dashboard_session_context(message=f'The account with Id {account_id} does not exist', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_update_customer_account_details.html',
            title='Add Customer Product', message_action='You can add a new customer ', hyperlink_text='here', hyperlink_url='BackOfficeApp:add_customer', modal_close_url='BackOfficeApp:get_accounts')
        dashboard_session_context.customer_account_id = account_id
        dashboard_session_context.add_account_form = accountRegistrationForm
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
    
    if request.POST:
           
           #This is for removing unwanted date format, 2022-08-30 00:00:00
            payment_due_date = request.POST['payment_due_date']
            payment_due_date  = payment_due_date.replace(' 00:00:00','')
            _mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['payment_due_date'] = payment_due_date
            request.POST._mutable = _mutable

            accountRegistrationForm = AccountRegistrationForm(request.POST, use_required_attribute=False)
            dashboard_session_context.add_account_form = accountRegistrationForm

            if accountRegistrationForm.is_valid():
                accountRegistrationForm = AccountRegistrationForm(request.POST, use_required_attribute=False, instance=account)
        
                accountRegistrationForm.save()
                
                dashboard_session_context = get_dashboard_session_context( display_template='AdminDashboard/dashboard_update_customer_account_details.html',
                message='The account details were successfully updated', message_class='add_customer_message_class_success', message_action='You can view details ', title='Update Account', hyperlink_text='here.', 
                hyperlink_url='BackOfficeApp:update_customer_account', add_account_form = accountRegistrationForm, modal_close_url='BackOfficeApp:get_accounts', hyperlink_url_parameters=account_id)
                dashboard_session_context.customer_account_id = account.id
                return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})

            return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})


    accountRegistrationForm = AccountRegistrationForm(account.__dict__, use_required_attribute=False)
    dashboard_session_context.add_account_form = accountRegistrationForm

    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
def get_accounts(request):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_all_accounts_landing_page.html')
    accounts = Account.objects.all()
    dashboard_session_context.all_customers_accounts = accounts
    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
def add_customer_account(request, id_number):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_add_customer_account.html', hyperlink_url_parameters=id_number, hyperlink_url='BackOfficeApp:delete_customer_account')
    
    dashboard_session_context.customer_id_number = id_number
    customer = Customer.objects.filter(id_number = id_number).first()
    accountRegistrationForm = AccountRegistrationForm(use_required_attribute=False)
    
    if not customer:
        dashboard_session_context = get_dashboard_session_context(message=f'The customer with Id number {id_number} does not exist', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_add_customer_account.html',
            title='Add Customer Account', message_action='You can add a new customer ', hyperlink_text='here', hyperlink_url='BackOfficeApp:add_customer', modal_close_url='BackOfficeApp:get_customers')
        dashboard_session_context.customer_id_number = id_number
        dashboard_session_context.add_account_form = accountRegistrationForm
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
    
    if request.POST:
           #This is for removing unwanted date format, 2022-08-30 00:00:00
            payment_due_date = request.POST['payment_due_date']
            payment_due_date  = payment_due_date.replace(' 00:00:00','')
            _mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['payment_due_date'] = payment_due_date
            request.POST._mutable = _mutable

            accountRegistrationForm = AccountRegistrationForm(request.POST, use_required_attribute=False)
            dashboard_session_context.add_account_form = accountRegistrationForm

            if accountRegistrationForm.is_valid():
                accountRegistrationForm = AccountRegistrationForm(request.POST, use_required_attribute=False)
                account = accountRegistrationForm.save(commit=False)
                account.customer = customer
                account.save()
                
                dashboard_session_context = get_dashboard_session_context( display_template='AdminDashboard/dashboard_add_customer_account.html',
                message='The account details were successfully added', message_class='add_customer_message_class_success', message_action='You can view details ', title='Add Account', hyperlink_text='here.', 
                hyperlink_url='BackOfficeApp:update_customer_account', add_account_form = accountRegistrationForm, modal_close_url='BackOfficeApp:get_accounts', hyperlink_url_parameters=account.id)
                dashboard_session_context.customer_id_number = id_number
                return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})

            return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})


    accountRegistrationForm = AccountRegistrationForm(use_required_attribute=False)
    dashboard_session_context.add_account_form = accountRegistrationForm

    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})

#AccountItem
def get_account_product(request, account_id):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_account_products.html')
    account_item = AccountItem.objects.filter(account__id__exact=account_id).first()
    print(account_item)   
 
    if not account_item:
        dashboard_session_context = get_dashboard_session_context(message='Oops! The account does not have any products associated with it.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_account_products.html',
                title='Customer Account Product', modal_close_url='BackOfficeApp:get_accounts', message_action='You can add a new product ', hyperlink_text='here',  hyperlink_url='BackOfficeApp:add_account_product', query_string=f'account_id={account_id}')
        dashboard_session_context.customer_id_number = 68
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
        

    dashboard_session_context.all_account_products = account_item.product_item.all()
    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})

#Category
def add_product_category(request):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_add_product_category.html',
    title='Add Product Category')
    productCategoryForm = ProductCategoryForm(use_required_attribute=False)
    dashboard_session_context.add_product_category = productCategoryForm

    if request.POST:
        productCategoryForm = ProductCategoryForm(request.POST, use_required_attribute=False)
        dashboard_session_context.add_product_category = productCategoryForm
        if productCategoryForm.is_valid():
            productCategoryForm.save()
            dashboard_session_context = get_dashboard_session_context(message='The product category was successfully added!', message_class='add_customer_message_class_success',  display_template ='AdminDashboard/dashboard_add_product_category.html',
                title='Add Customer Product', hyperlink_text='here', message_action = 'You can update the details ',  hyperlink_url='BackOfficeApp:update_product_category', modal_close_url='BackOfficeApp:get_product_categories', hyperlink_url_parameters=productCategoryForm.instance.id)
            dashboard_session_context.add_product_category = productCategoryForm
           
    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
def update_product_category(request, category_id):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_update_product_category.html',
    title='Update Product Category')
    dashboard_session_context.product_category_id = category_id

    category = ProductCategory.objects.filter(id = category_id).first()
    if not category:
        productCategoryForm = ProductCategoryForm(use_required_attribute=False)
        dashboard_session_context = get_dashboard_session_context(message=f'The category with Id {category_id} does not exist.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_update_product_category.html',
            title='Update Product Category', message_action='You can add a new category ', hyperlink_text='here', hyperlink_url='BackOfficeApp:add_product_category', modal_close_url='BackOfficeApp:get_product_categories')
        dashboard_session_context.add_product_category = productCategoryForm
        dashboard_session_context.product_category_id = category_id
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})

    if request.POST:
        productCategoryForm = ProductCategoryForm(request.POST, instance=category)
        dashboard_session_context.add_product_category = productCategoryForm
        if productCategoryForm.is_valid():
            productCategoryForm.save()
            dashboard_session_context = get_dashboard_session_context(message='The product category was successfully updated!', message_class='add_customer_message_class_success',  display_template ='AdminDashboard/dashboard_update_product_category.html',
                title='Update Customer Product', hyperlink_text='here', message_action = 'You can update the details ',  hyperlink_url='BackOfficeApp:update_product_category', modal_close_url='BackOfficeApp:get_product_categories', hyperlink_url_parameters=productCategoryForm.instance.id)
            dashboard_session_context.add_product_category = productCategoryForm
            dashboard_session_context.product_category_id = category_id
            return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
    
    productCategoryForm = ProductCategoryForm(category.__dict__)
    dashboard_session_context.add_product_category = productCategoryForm
    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
def delete_product_category(request, category_id):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_update_product_category.html',
    title='Delete Product Category')
    
    category = ProductCategory.objects.filter(id = category_id)
    if not category:
        productCategoryForm = ProductCategoryForm(use_required_attribute=False)
        dashboard_session_context = get_dashboard_session_context(message=f'The category with Id {category_id} does not exist', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_update_product_category.html',
            title='Delete Product Category', message_action='You can add a new category ', hyperlink_text='here', hyperlink_url='BackOfficeApp:add_product_category', modal_close_url='BackOfficeApp:get_product_categories')
        dashboard_session_context.add_product_category = productCategoryForm
        dashboard_session_context.product_category_id = category_id
    else:
        category.delete()
        productCategoryForm = ProductCategoryForm(use_required_attribute=False)
        dashboard_session_context = get_dashboard_session_context(message=f'The category was successfully deleted', message_class='add_customer_message_class_success',  display_template ='AdminDashboard/dashboard_update_product_category.html',
            title='Delete Product Category',  modal_close_url='BackOfficeApp:get_product_categories')
        dashboard_session_context.add_product_category = productCategoryForm
        dashboard_session_context.product_category_id = category_id

    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
def get_product_categories(request):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_category_landing_page.html')
    dashboard_session_context.product_categories = ProductCategory.objects.all()

    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})


#Products
def get_all_customers_products(request):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_customer_products_landing_page.html')
    dashboard_session_context.all_customers_products = ProductItem.objects.all()
    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
def update_customer_product(request, product_id):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_update_customer_product.html')
    dashboard_session_context.customer_product_id = product_id

    product = ProductItem.objects.filter(id=product_id).first()

    if not product:
        productItemForm = ProductItemForm(use_required_attribute=False)
        dashboard_session_context = get_dashboard_session_context(message=f'The product with Id {product_id} does not exist.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_update_customer_product.html',
            title='Update Product', message_action='You can add a new product ', hyperlink_text='here', hyperlink_url='BackOfficeApp:add_customer_product', modal_close_url='BackOfficeApp:get_all_customers_products')
        dashboard_session_context.update_customer_product_form = productItemForm
        dashboard_session_context.customer_product_id = product_id
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
    
    if request.POST:
        productItemForm = ProductItemForm(request.POST, use_required_attribute=False, instance=product)
        dashboard_session_context.update_customer_product_form = productItemForm
        if productItemForm.is_valid():
            productItemForm.save()
            dashboard_session_context = get_dashboard_session_context(message='The customer product was successfully updated!', message_class='add_customer_message_class_success',  display_template ='AdminDashboard/dashboard_update_customer_product.html',
                title='Update Customer Product', hyperlink_text='here', message_action = 'You can view details ',  hyperlink_url='BackOfficeApp:update_customer_product', modal_close_url='BackOfficeApp:get_all_customers_products', hyperlink_url_parameters=product_id)
            dashboard_session_context.customer_product_id = product_id
            dashboard_session_context.update_customer_product_form = productItemForm
            return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})

    item_dictionary = product.__dict__
    item_dictionary['category'] = product.category
    productItemForm = ProductItemForm(item_dictionary, use_required_attribute=False)
    dashboard_session_context.update_customer_product_form = productItemForm

    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
def delete_customer_product(request, product_id):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_update_customer_product.html')
    
    product = ProductItem.objects.filter(id=product_id).first()
    if not product:
        productItemForm = ProductItemForm(use_required_attribute=False)
        dashboard_session_context = get_dashboard_session_context(message=f'The product with Id {product_id} does not exist.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_update_customer_product.html',
            title='Update Product', message_action='You can add a new product ', hyperlink_text='here', hyperlink_url='BackOfficeApp:add_customer_product', modal_close_url='BackOfficeApp:get_all_customers_products')
        dashboard_session_context.update_customer_product_form = productItemForm
        dashboard_session_context.customer_product_id = product_id
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
    else:
        product.delete()
        productItemForm = ProductItemForm(use_required_attribute=False)
        dashboard_session_context = get_dashboard_session_context(message=f'The product was successfully deleted', message_class='add_customer_message_class_success',  display_template ='AdminDashboard/dashboard_update_customer_product.html',
            title='Delete Product',  modal_close_url='BackOfficeApp:get_all_customers_products')
        dashboard_session_context.update_customer_product_form = productItemForm
        dashboard_session_context.customer_product_id = product_id

    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
def add_customer_product(request):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_add_customer_product.html')
    productItemForm = ProductItemForm(use_required_attribute=False)
    dashboard_session_context.add_customer_product_form = productItemForm

    if request.POST:
        productItemForm = ProductItemForm(request.POST, use_required_attribute=False)
        dashboard_session_context.add_customer_product_form = productItemForm
        if productItemForm.is_valid():
            productItemForm.save()
            
            dashboard_session_context = get_dashboard_session_context(message='The customer product was successfully added!', message_class='add_customer_message_class_success',  display_template ='AdminDashboard/dashboard_add_customer_product.html',
                title='Add Customer Product', hyperlink_text='here', message_action = 'You can view details ',  hyperlink_url='BackOfficeApp:update_customer_product', modal_close_url='BackOfficeApp:get_all_customers_products', hyperlink_url_parameters=productItemForm.instance.id)
            dashboard_session_context.add_customer_product_form = productItemForm
            return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})


