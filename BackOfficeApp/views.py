from unicodedata import category
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
                hyperlink_url='BackOfficeApp:addproduct', query_string=f'account_id={account.id}', add_account_form = accountRegistrationForm, add_customer_form = customerRegistrationForm, modal_close_url='BackOfficeApp:customers')
                
            else:
                dashboard_session_context = get_dashboard_session_context('AdminDashboard/dashboard_customer_registration.html',
                message='An account with the same ID number already exists. Choose a different one.', message_class='add_customer_message_class_error', message_action='You can update the customer information ', title='Customer Registration', hyperlink_text='here.', 
                hyperlink_url='BackOfficeApp:updatecustomer', hyperlink_url_parameters=id, add_account_form = accountRegistrationForm, add_customer_form = customerRegistrationForm, modal_close_url='BackOfficeApp:customers')
                

    return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})

def update_customer_product(request, account_id):
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

def add_customer_product(request):
    account_id = int(request.GET.get('account_id', -1))
    account = Account.objects.filter(id = account_id).first()
    number_of_products = 0 if not account  else account.number_of_products

    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_customer_add_product_item.html',
    title='Add Customer Product', post_form_parameters = f'account_id={account_id}&number_of_products={number_of_products}')
   
    dashboard_session_context.add_product_forms_list = get_products_forms(request, number_of_products if number_of_products > 0 else 1)
    
    if not account:
        list =  dashboard_session_context.add_product_forms_list
        dashboard_session_context = get_dashboard_session_context(message=f'The account with Id {account_id} does not exist', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_customer_add_product_item.html',
            title='Add Customer Product', message_action='You can add a new customer ', hyperlink_text='here', hyperlink_url='BackOfficeApp:addcustomer', modal_close_url='BackOfficeApp:customers')
        dashboard_session_context.add_product_forms_list = list
        return render (request, 'AdminDashboard/admin_dashboard.html', {'dashboard_session': dashboard_session_context})
    
    if request.POST:
        if is_a_duplicate_request(request):
            list =  dashboard_session_context.add_product_forms_list
            dashboard_session_context = get_dashboard_session_context(message=f'Oops! You have already added the same product(s) for the customer with account Id({account_id}) ', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_customer_add_product_item.html',
            title='Add Customer Product', message_action='You can update the customer product details', hyperlink_text='here', hyperlink_url='BackOfficeApp:updateproduct', hyperlink_url_parameters = account_id, modal_close_url='BackOfficeApp:customers')
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
                dashboard_session_context = get_dashboard_session_context(message='A customer with the provided ID number does not exist.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/dashboard_customer_add_product_item.html',
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
                
                dashboard_session_context = get_dashboard_session_context(message='The customer product was successfully added!', message_class='add_customer_message_class_success',  display_template ='AdminDashboard/dashboard_customer_add_product_item.html',
                title='Add Customer Product', hyperlink_text='here', message_action = 'You can add a new customer',  hyperlink_url='BackOfficeApp:addcustomer', modal_close_url='BackOfficeApp:customers')
                
                dashboard_session_context.add_product_forms_list = get_products_forms(request, number_of_products)
                
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
            print(dashboard_session_context.add_product_category)
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

 

