from django.shortcuts import render
from BackOfficeApp.utils.customers.customer import get_dashboard_session_context
from BackOfficeApp.models.customer.models import *
from BackOfficeApp.models.customer.forms import *
from BackOfficeApp.models.account.models import *
from BackOfficeApp.models.account.forms import *
from BackOfficeApp.models.product.models import *
from BackOfficeApp.models.product.forms import *
import hashlib
import json

#Helper Methods
def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s_%s_%s.%s" % (instance.product_item.name, instance.product_item.year,'productItemId', instance.product_item.id, ext)
    return os.path.join('product_images', filename)

def get_request_hash_value(request):
    form_data_string = f'{str(request.POST)}{str(request.FILES)}'
    hash_object = hashlib.sha256(json.dumps(form_data_string).encode())
    return hash_object.hexdigest()

def is_a_duplicate_request(request):
    account = ProductRequest.objects.filter(hash_value=get_request_hash_value(request))
    if not account:
        return False
    return True

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

    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/account/add_account_products.html',
    title='Add Customer Product', post_form_parameters = f'account_id={account_id}&number_of_products={number_of_products}')
   
    dashboard_session_context.add_product_forms_list = get_products_forms(request, number_of_products if number_of_products > 0 else 1)
    dashboard_session_context.number_of_products = number_of_products
    if not account:
        list =  dashboard_session_context.add_product_forms_list
        dashboard_session_context = get_dashboard_session_context(message=f'The account with Id {account_id} does not exist', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/account/add_account_products.html',
            title='Add Customer Product', message_action='You can add a new customer ', hyperlink_text='here', hyperlink_url='BackOfficeApp:add_customer', modal_close_url='BackOfficeApp:get_all_customers')
        dashboard_session_context.add_product_forms_list = list
        return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
    
    if request.POST:
        if is_a_duplicate_request(request):
            list =  dashboard_session_context.add_product_forms_list
            dashboard_session_context = get_dashboard_session_context(message=f'Oops! You have already added the same product(s) for the customer with account Id({account_id}) ', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/account/add_account_products.html',
            title='Add Customer Product', message_action='You can update the customer product details', hyperlink_text='here', hyperlink_url='BackOfficeApp:get_account_product', hyperlink_url_parameters = account_id, modal_close_url='BackOfficeApp:get_all_customers')
            dashboard_session_context.add_product_forms_list = list
            dashboard_session_context.number_of_products = number_of_products
           
            return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
        
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
                dashboard_session_context = get_dashboard_session_context(message='A customer with the provided ID number does not exist.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/account/add_account_products.html',
                title='Add Customer Product', hyperlink_text='here', message_action = 'You can add a new customer',  hyperlink_url='BackOfficeApp:add_customer', modal_close_url='BackOfficeApp:get_all_customers')
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
                
                dashboard_session_context = get_dashboard_session_context(message='The customer product was successfully added!', message_class='add_customer_message_class_success',  display_template ='AdminDashboard/account/add_account_products.html',
                title='Add Customer Product', hyperlink_text='here', message_action = 'You can add a new customer',  hyperlink_url='BackOfficeApp:add_customer', modal_close_url='BackOfficeApp:get_all_customers')
                
                dashboard_session_context.add_product_forms_list = get_products_forms(request, number_of_products)
                dashboard_session_context.number_of_products = number_of_products
    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
def get_customer_accounts(request, id_number):
    customer = Customer.objects.filter(id_number=id_number).first()
    customerRegistrationForm = CustomerRegistrationForm(use_required_attribute=False)
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/account/show_customer_accounts.html')
    dashboard_session_context.customer_id_number = id_number

    if not customer:
        dashboard_session_context = get_dashboard_session_context(message='Oops! The customer you provided does not exist.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/account/show_customer_accounts.html',
                title='Customer Account', add_customer_form = customerRegistrationForm, modal_close_url='BackOfficeApp:get_all_customers', post_form_parameters = id_number)
        dashboard_session_context.customer_id_number = id_number
        return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})

    accounts = Account.objects.select_related('customer').filter(customer__id_number__exact=id_number)
    dashboard_session_context.all_customers_accounts = accounts

    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
def update_customer_account(request, account_id):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/account/update_customer_account.html', hyperlink_url_parameters=account_id, hyperlink_url='BackOfficeApp:delete_customer_account')
    
    dashboard_session_context.customer_account_id = account_id
    account = Account.objects.filter(id = account_id).first()
    accountRegistrationForm = AccountRegistrationForm(use_required_attribute=False)
    
    if not account:
        dashboard_session_context = get_dashboard_session_context(message=f'The account with Id {account_id} does not exist', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/account/update_customer_account.html',
            title='Add Customer Product', message_action='You can add a new customer ', hyperlink_text='here', hyperlink_url='BackOfficeApp:add_customer', modal_close_url='BackOfficeApp:get_accounts')
        dashboard_session_context.customer_account_id = account_id
        dashboard_session_context.add_account_form = accountRegistrationForm
        return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
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
                
                dashboard_session_context = get_dashboard_session_context( display_template='AdminDashboard/account/update_customer_account.html',
                message='The account details were successfully updated', message_class='add_customer_message_class_success', message_action='You can view details ', title='Update Account', hyperlink_text='here.', 
                hyperlink_url='BackOfficeApp:update_customer_account', add_account_form = accountRegistrationForm, modal_close_url='BackOfficeApp:get_all_accounts', hyperlink_url_parameters=account_id)
                dashboard_session_context.customer_account_id = account.id
                return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})

            return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})


    accountRegistrationForm = AccountRegistrationForm(account.__dict__, use_required_attribute=False)
    dashboard_session_context.add_account_form = accountRegistrationForm

    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
def get_all_accounts(request):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/account/show_customer_accounts.html')
    accounts = Account.objects.all()
    dashboard_session_context.all_customers_accounts = accounts
    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
def add_customer_account(request, id_number):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_add_customer_account.html', hyperlink_url_parameters=id_number, hyperlink_url='BackOfficeApp:delete_customer_account')
    
    dashboard_session_context.customer_id_number = id_number
    customer = Customer.objects.filter(id_number = id_number).first()
    accountRegistrationForm = AccountRegistrationForm(use_required_attribute=False)
    
    if not customer:
        dashboard_session_context = get_dashboard_session_context(message=f'The customer with Id number {id_number} does not exist', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_add_customer_account.html',
            title='Add Customer Account', message_action='You can add a new customer ', hyperlink_text='here', hyperlink_url='BackOfficeApp:add_customer', modal_close_url='BackOfficeApp:get_all_customers')
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
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/account/show_account_products.html')
    account_item = AccountItem.objects.filter(account__id__exact=account_id).first()
    print(account_item)   
 
    if not account_item:
        dashboard_session_context = get_dashboard_session_context(message='Oops! The account does not have any products associated with it.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/account/show_account_products.html',
                title='Customer Account Product', modal_close_url='BackOfficeApp:get_accounts', message_action='You can add a new product ', hyperlink_text='here',  hyperlink_url='BackOfficeApp:add_account_product', query_string=f'account_id={account_id}')
        dashboard_session_context.customer_id_number = 68
        return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
        

    dashboard_session_context.all_account_products = account_item.product_item.all()
    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})

def delete_customer_account(request, account_id):
    #try:
        dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_account_products.html')
        customerRegistrationForm = CustomerRegistrationForm(use_required_attribute=False)
        accountRegistrationForm = AccountRegistrationForm(use_required_attribute=False)
        dashboard_session_context.add_customer_post_form_parameters = account_id
        dashboard_session_context.display_template = 'AdminDashboard/account/update_customer_account.html'
        dashboard_session_context.add_customer_form = customerRegistrationForm
        dashboard_session_context.add_account_form = accountRegistrationForm
        dashboard_session_context.customer_account_id = account_id   

        account = Account.objects.filter(id=account_id).first()
        
        if not account:
            dashboard_session_context = get_dashboard_session_context(message='Oops! The account you provided does not exist.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_update_customer_account_detailsr.html',
                title='Delete Account', add_customer_form = customerRegistrationForm, add_account_form = accountRegistrationForm, modal_close_url='BackOfficeApp:get_all_customers', post_form_parameters = id_number)
            dashboard_session_context.customer_account_id = account_id 
            return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})

        account.delete()
        dashboard_session_context.add_customer_message  = 'The account was successfully deleted!'
        dashboard_session_context.add_customer_message_class  = 'add_customer_message_class_success'
        
        return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
    #except Exception as e:
       # print(e)