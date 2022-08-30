from django.shortcuts import render
from BackOfficeApp.utils.customers.customer import get_dashboard_session_context
from BackOfficeApp.models.product.models import *
from BackOfficeApp.models.product.forms import *
from BackOfficeApp.models.customer.forms import *


#Products
def get_all_customers_products(request):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/product/show_products.html')
    dashboard_session_context.all_customers_products = ProductItem.objects.all()
    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
def update_customer_product(request, product_id):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/product/update_account_product.html')
    dashboard_session_context.customer_product_id = product_id

    product = ProductItem.objects.filter(id=product_id).first()
    image = ProductItemImage.objects.filter(product_item_id = product_id).first()

    if not product:
        productItemForm = ProductItemForm(use_required_attribute=False)
        productItemImageForm = ProductItemImageForm(use_required_attribute=False)
        keepProductImage = KeepProductImageForm(use_required_attribute=False)
        dashboard_session_context = get_dashboard_session_context(message=f'The asset with Id {product_id} does not exist.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/product/update_account_product.html',
            title='Update Asset', message_action='You can add a new asset ', hyperlink_text='here', hyperlink_url='BackOfficeApp:add_customer_product', modal_close_url='BackOfficeApp:get_all_customers_products')
        dashboard_session_context.update_customer_product_form = productItemForm
        dashboard_session_context.add_product_image_form= productItemImageForm
        dashboard_session_context.keep_product_image_form= keepProductImage
        dashboard_session_context.customer_product_id = product_id
        return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
    if request.POST:
        productItemForm = ProductItemForm(request.POST, use_required_attribute=False)
        productItemImageForm = ProductItemImageForm(request.POST, request.FILES, use_required_attribute=False)
        keepProductImage = KeepProductImageForm(request.POST, use_required_attribute=False)
        dashboard_session_context.update_customer_product_form = productItemForm
        dashboard_session_context.add_product_image_form= productItemImageForm
        dashboard_session_context.keep_product_image_form= keepProductImage
        
        all_forms_are_valid = True
        keep_product_image = keepProductImage.save(commit=False).keep_image

        if not productItemForm.is_valid():
            all_forms_are_valid = False
        elif not productItemImageForm.is_valid() and not keep_product_image:
                    all_forms_are_valid = False

        if all_forms_are_valid:
            productItemForm = ProductItemForm(request.POST, use_required_attribute=False, instance=product)
            productItemImageForm = ProductItemImageForm(request.POST, request.FILES, use_required_attribute=False, instance=image)
            productItemForm.save()
            productItemImageForm.save()
            

            dashboard_session_context = get_dashboard_session_context(message='The customer asset was successfully updated!', message_class='add_customer_message_class_success',  display_template ='AdminDashboard/product/update_account_product.html',
                title='Update Customer Asset', hyperlink_text='here', message_action = 'You can view details ',  hyperlink_url='BackOfficeApp:update_customer_product', modal_close_url='BackOfficeApp:get_all_customers_products', hyperlink_url_parameters=product_id)
            dashboard_session_context.customer_product_id = product_id
            dashboard_session_context.update_customer_product_form = productItemForm
            dashboard_session_context.add_product_image_form= productItemImageForm
            dashboard_session_context.keep_product_image_form= keepProductImage
            return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
        
        if keep_product_image:
            productItemImageForm = ProductItemImageForm(request.POST, request.FILES, use_required_attribute=False, instance=image)
            dashboard_session_context.add_product_image_form= productItemImageForm
            dashboard_session_context.keep_product_image = image.image
        return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})

    item_dictionary = product.__dict__
    item_dictionary['category'] = product.category
    
    productItemForm = ProductItemForm(item_dictionary, use_required_attribute=False)
    productItemImageForm = ProductItemImageForm(use_required_attribute=False)
    keepProductImage = KeepProductImageForm(use_required_attribute=False)
    
    dashboard_session_context.add_product_image_form= productItemImageForm
    dashboard_session_context.update_customer_product_form = productItemForm
    dashboard_session_context.keep_product_image_form= keepProductImage
    dashboard_session_context.keep_product_image = image.image

    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
def delete_customer_product(request, product_id):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/dashboard_update_customer_product.html')
    
    product = ProductItem.objects.filter(id=product_id).first()
    if not product:
        productItemForm = ProductItemForm(use_required_attribute=False)
        dashboard_session_context = get_dashboard_session_context(message=f'The asset with Id {product_id} does not exist.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/product/update_account_product.html',
            title='Update Asset', message_action='You can add a new asset ', hyperlink_text='here', hyperlink_url='BackOfficeApp:add_customer_product', modal_close_url='BackOfficeApp:get_all_customers_products')
        dashboard_session_context.update_customer_product_form = productItemForm
        dashboard_session_context.customer_product_id = product_id
        return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
    else:
        product.delete()
        productItemForm = ProductItemForm(use_required_attribute=False)
        dashboard_session_context = get_dashboard_session_context(message=f'The asset was successfully deleted', message_class='add_customer_message_class_success',  display_template ='AdminDashboard/product/update_account_product.html',
            title='Delete Asset',  modal_close_url='BackOfficeApp:get_all_customers_products')
        dashboard_session_context.update_customer_product_form = productItemForm
        dashboard_session_context.customer_product_id = product_id

    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
def add_customer_product(request):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/product/add_customer_product.html')
    product_item_form = ProductItemForm(use_required_attribute=False)
    product_item_image_form = ProductItemImageForm(use_required_attribute=False)
    link_asset_form= LinkProductWithCustomerForm(use_required_attribute=False)
    customer_asset_form = CustomerAssetForm(use_required_attribute=False)
    

    dashboard_session_context.add_customer_product_form = product_item_form
    dashboard_session_context.add_product_image_form= product_item_image_form
    dashboard_session_context.link_asset_with_customer_form= link_asset_form
    dashboard_session_context.customer_asset_form = customer_asset_form

    if request.POST:
        product_item_form = ProductItemForm(request.POST, use_required_attribute=False)
        product_item_image_form = ProductItemImageForm(request.POST, request.FILES, use_required_attribute=False)
        link_asset_form= LinkProductWithCustomerForm(request.POST, use_required_attribute=False)
        customer_asset_form = CustomerAssetForm(request.POST, use_required_attribute=False)
        dashboard_session_context.add_customer_product_form = product_item_form
        dashboard_session_context.add_product_image_form= product_item_image_form
        dashboard_session_context.link_asset_with_customer_form= link_asset_form
        dashboard_session_context.customer_asset_form = customer_asset_form
       
        all_forms_are_valid = True
        link_asset = link_asset_form.save(commit=False).link_product_with_customer
        if not customer_asset_form.is_valid() and link_asset:
            all_forms_are_valid = False
        elif not product_item_form.is_valid() and not product_item_image_form.is_valid():
             all_forms_are_valid = False
        
        if all_forms_are_valid:
            item = product_item_form.save()
            image = product_item_image_form.save(commit=False)
            image.product_item = item
            image.save()

            if link_asset:
                asset = customer_asset_form.save(commit=False)
                customer_asset = CustomerAsset(customer = asset.customer, product_item = item)
                customer_asset.save()

            dashboard_session_context = get_dashboard_session_context(message='The customer asset was successfully added!', message_class='add_customer_message_class_success',  display_template ='AdminDashboard/product/add_customer_product.html',
                title='Add Customer Asset', hyperlink_text='here', message_action = 'You can view details ',  hyperlink_url='BackOfficeApp:update_customer_product', modal_close_url='BackOfficeApp:get_all_customers_products', hyperlink_url_parameters=item.id)
            dashboard_session_context.add_customer_product_form = product_item_form
            dashboard_session_context.add_product_image_form= product_item_image_form
            dashboard_session_context.link_asset_with_customer_form = link_asset_form
            dashboard_session_context.customer_asset_form = customer_asset_form
            return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
        customer_asset_form = CustomerAssetForm(use_required_attribute=False)
        link_asset_form= LinkProductWithCustomerForm(use_required_attribute=False)
        dashboard_session_context.link_asset_with_customer_form= link_asset_form
        dashboard_session_context.customer_asset_form = customer_asset_form
        return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})


#Categories