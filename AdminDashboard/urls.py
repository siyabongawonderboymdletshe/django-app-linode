from django.urls import path, include
from .views import admin_dashboard

app_name = 'AdminDashboard'

urlpatterns = [
    path('', view=admin_dashboard, name='adminlandingpage'),
]
