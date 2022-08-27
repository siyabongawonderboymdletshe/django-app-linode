from .models import *

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