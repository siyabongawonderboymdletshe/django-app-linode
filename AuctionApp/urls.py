from django.urls import path
from .views import items, buyitem, login, registerclient


app_name = 'AuctionApp'

urlpatterns = [
    path('', view=items, name='home'),
    path('items', view=items, name='items'),
    path('buyitem/<int:id>', view = buyitem, name='buyitem'),
    path('login', view=login, name='login'),
    path('registerclient', view=registerclient, name='registerclient'),
]
