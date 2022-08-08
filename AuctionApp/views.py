from urllib import response
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Item, RegistrationForm, LoginForm, ItemBuyer, PaymentRequestData
from django.db.models import Case, When
from django.db.models import CharField
from django.core.mail import send_mail
from DjangoApp import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime
from utils.payfast import payfast

def paymentreturn(request):
    return render (request, 'AuctionApp/payment_return.html')
def paymentcancel(request):
    return render (request, 'AuctionApp/payment_cancel.html')

@csrf_exempt 
def paymentnotify(request, user_id, item_id):
    item = Item.objects.get(id = item_id)
    is_payfast_payment_successful = payfast.is_payfast_payment_successful(request, item.amount)
    if is_payfast_payment_successful:
        print('payment was successful....')
        buyerUser = User.objects.get(id = user_id)
        buyer = ItemBuyer()
        buyer.user = buyerUser
        buyer.save()

        item.status = 'SOLD'
        item.save()

        buyer.items.add(item)
        
        send_mail(
            'Testing My Django App',
            f'Hello {buyerUser}. Thank you for purchasing the following with us:\n {item.name} \n {item.description} \n {item.amount} ',
            settings.EMAIL_HOST_USER,
            [buyerUser.email],
            fail_silently=True,
        )
        print('email sent....')
    else:
        print('payment was not successful....')

    return render (request, 'AuctionApp/payment_notify.html')
def items(request):
    items = Item.objects.annotate(
            relevancy=Case(When(status='AVAILABLE', then=3), When(status='SOLD', then=2), When(status='UNAVAILABLE', then=1), output_field=CharField())
        ).order_by('-relevancy').values()

    request.session['items'] = list(items)
    return render (request, 'AuctionApp/items.html')

def buyitem(request, id):
    try:
        user = request.session.get('active_user', None)
        if user:
            if user['is_active'] == True:
             
                item = Item.objects.get(id=id)   
                
                paysafe_payment_data = payfast.get_paysafe_payment_data(user, item)
                request_data = PaymentRequestData(signature = paysafe_payment_data['signature'], data = payfast.dataToString(paysafe_payment_data), date_time = datetime.now())
                request_data.save()
                
                request.session['paysafe_payment'] = paysafe_payment_data

                return render (request, 'AuctionApp/payment_redirect.html', {'paysafe_payment_data': paysafe_payment_data}) 
            #user is not active. Block the purchase
            extradata = {
                    'message':  'You need to be an active user to be able to make a purchase.',
                    'id': 0,
                    'title': 'Inactive User'
                }
            return render (request, 'AuctionApp/items.html', {'extradata': extradata})    
        return HttpResponseRedirect( "%s?buyitemid=%s" % (reverse('AuctionApp:login'), id))
    except Exception as e:
        print(e)
        extradata = {
                    'message':  'Opps! Something went wrong while processing your request. Please try again or contact our support if the issue persists.',
                    'id': 1,
                    'title': 'Purchasing Error'
                }
        return render (request, 'AuctionApp/items.html', {'extradata': extradata})
        
def login(request):
    try:
        if request.POST:
            form = LoginForm(request.POST, use_required_attribute=False)
            if form.is_valid():
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                if user is not None:
                    request.session['active_user'] = {
                        'id' : user.id,
                        'first_name' : user.first_name,
                        'last_name' : user.last_name, 
                        'username' : user.username, 
                        'email' : user.email,
                        'password' : user.password, 
                        'is_active': user.is_active}
                    if request.GET.get("buyitemid"):
                        return HttpResponseRedirect(reverse('AuctionApp:buyitem', args=[request.GET.get("buyitemid")]), request)
                    return HttpResponseRedirect(reverse('AuctionApp:items'))
                extradata = {
                        'message': 'An account with the provided details does not exists. Enter your valid details or',
                        'id': 2,
                         'title': 'Unknown Account'
                    }
                print(extradata)
                return render (request, 'AuctionApp/login.html', {'form':form, 'extradata': extradata})
            return render (request, 'AuctionApp/login.html', {'form':form})
        form = LoginForm(use_required_attribute=False)  
        return render (request, 'AuctionApp/login.html', {'form':form})
    
    except Exception as e:
        print(e)
        extradata = {
                    'message':  'Something went wrong while processing your login request. Please try again or contact our support if the issue persists.',
                    'id': 3,
                     'title': 'Login Error'
                }
        return render (request, 'AuctionApp/login.html', {'form':form, 'extradata': extradata})    
def registerclient(request):
    try:
        if request.POST:
            form = RegistrationForm(request.POST, use_required_attribute=False)
            if form.is_valid():
                print('form is valid')
                #user = User.objects.get(username = request.POST['username'])
                user = User.objects.filter(username = request.POST['username'])
                print(user)
                if not user:
                    user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
                    user.first_name = request.POST['firstname']
                    user.last_name = request.POST['lastname']
                    user.save()
                    return HttpResponseRedirect(reverse('AuctionApp:items'))
                extradata = {
                    'message': 'An account with the same username already exists. Choose a different one or',
                    'id': 4,
                     'title': 'Existing Account'
                }
                return render (request, 'AuctionApp/registration.html', {'form':form, 'extradata': extradata})
            return render (request, 'AuctionApp/registration.html', {'form':form})
        
        form = RegistrationForm(use_required_attribute=False)  
        return render (request, 'AuctionApp/registration.html', {'form':form})
    except Exception as e:
        print(e)
        extradata = {
                    'message':  'Something went wrong while processing your registration request. Please try again or contact our support if the issue persists.',
                    'id': 5,
                     'title': 'Registration Error'
                }
        return render (request, 'AuctionApp/registration.html', {'form':form, 'extradata': extradata})