from django.urls import path, include
from .views import *

app_name = 'AdminDashboard'

urlpatterns = [
    path('', view=admin_dashboard, name='admin_dashboard_landing_page'),
    path('login', view=user_login, name='login'),
     path('register', view=user_registration, name='register'),
]
