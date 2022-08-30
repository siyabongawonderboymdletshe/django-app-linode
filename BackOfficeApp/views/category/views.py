from django.shortcuts import render
from BackOfficeApp.models.product.models import *
from BackOfficeApp.models.product.forms import *
from BackOfficeApp.utils.customers.customer import get_dashboard_session_context

#Category
def add_product_category(request):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/category/add_product_category.html',
    title='Add Product Category')
    productCategoryForm = ProductCategoryForm(use_required_attribute=False)
    dashboard_session_context.add_product_category = productCategoryForm

    if request.POST:
        productCategoryForm = ProductCategoryForm(request.POST, use_required_attribute=False)
        dashboard_session_context.add_product_category = productCategoryForm
        if productCategoryForm.is_valid():
            productCategoryForm.save()
            dashboard_session_context = get_dashboard_session_context(message='The product category was successfully added!', message_class='add_customer_message_class_success',  display_template ='AdminDashboard/category/add_product_category.html',
                title='Add Customer Product', hyperlink_text='here', message_action = 'You can update the details ',  hyperlink_url='BackOfficeApp:update_product_category', modal_close_url='BackOfficeApp:get_product_categories', hyperlink_url_parameters=productCategoryForm.instance.id)
            dashboard_session_context.add_product_category = productCategoryForm
    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})      

def update_product_category(request, category_id):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/category/update_product_category.html',
    title='Update Product Category')
    dashboard_session_context.product_category_id = category_id

    category = ProductCategory.objects.filter(id = category_id).first()
    if not category:
        productCategoryForm = ProductCategoryForm(use_required_attribute=False)
        dashboard_session_context = get_dashboard_session_context(message=f'The category with Id {category_id} does not exist.', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/update_product_category.html',
            title='Update Product Category', message_action='You can add a new category ', hyperlink_text='here', hyperlink_url='BackOfficeApp:add_product_category', modal_close_url='BackOfficeApp:get_product_categories')
        dashboard_session_context.add_product_category = productCategoryForm
        dashboard_session_context.product_category_id = category_id
        return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})

    if request.POST:
        productCategoryForm = ProductCategoryForm(request.POST, instance=category)
        dashboard_session_context.add_product_category = productCategoryForm
        if productCategoryForm.is_valid():
            productCategoryForm.save()
            dashboard_session_context = get_dashboard_session_context(message='The product category was successfully updated!', message_class='add_customer_message_class_success',  display_template ='AdminDashboard/update_product_category.html',
                title='Update Customer Product', hyperlink_text='here', message_action = 'You can update the details ',  hyperlink_url='BackOfficeApp:update_product_category', modal_close_url='BackOfficeApp:get_product_categories', hyperlink_url_parameters=productCategoryForm.instance.id)
            dashboard_session_context.add_product_category = productCategoryForm
            dashboard_session_context.product_category_id = category_id
            return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
    
    productCategoryForm = ProductCategoryForm(category.__dict__)
    dashboard_session_context.add_product_category = productCategoryForm
    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})
def delete_product_category(request, category_id):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/category/update_product_category.html',
    title='Delete Product Category')
    
    category = ProductCategory.objects.filter(id = category_id)
    if not category:
        productCategoryForm = ProductCategoryForm(use_required_attribute=False)
        dashboard_session_context = get_dashboard_session_context(message=f'The category with Id {category_id} does not exist', message_class='add_customer_message_class_error',  display_template ='AdminDashboard/category/update_product_category.html',
            title='Delete Product Category', message_action='You can add a new category ', hyperlink_text='here', hyperlink_url='BackOfficeApp:add_product_category', modal_close_url='BackOfficeApp:get_product_categories')
        dashboard_session_context.add_product_category = productCategoryForm
        dashboard_session_context.product_category_id = category_id
    else:
        category.delete()
        productCategoryForm = ProductCategoryForm(use_required_attribute=False)
        dashboard_session_context = get_dashboard_session_context(message=f'The category was successfully deleted', message_class='add_customer_message_class_success',  display_template ='AdminDashboard/category/update_product_category.html',
            title='Delete Product Category',  modal_close_url='BackOfficeApp:get_product_categories')
        dashboard_session_context.add_product_category = productCategoryForm
        dashboard_session_context.product_category_id = category_id
    return render (request, 'AdminDashboard/landing_page/sidebar.html', {'dashboard_session': dashboard_session_context})

def get_product_categories(request):
    dashboard_session_context = get_dashboard_session_context(display_template ='AdminDashboard/category/show_product_category.html')
    dashboard_session_context.product_categories = ProductCategory.objects.all()

    return render (request, 'AdminDashboard/landing_page/s``idebar.html', {'dashboard_session': dashboard_session_context})