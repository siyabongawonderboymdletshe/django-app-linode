from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Item, RegistrationForm, LoginForm
from django.db.models import Case, When
from django.db.models import CharField
# Create your views here.

def items(request):
    #items = Item.objects.order_by('status').values()

    
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
                item.status = 'SOLD'
                item.save()
                return HttpResponseRedirect(reverse('AuctionApp:items'))
            #user is not active. Block the purchase
            extradata = {
                    'message':  'You need to be an active user to be able to make a purchase.',
                    'id': 0,
                    'title': 'Inactive User'
                }
            return render (request, 'AuctionApp/items.html', {'extradata': extradata})    
        return HttpResponseRedirect( "%s?buyitemid=%s" % (reverse('AuctionApp:login'), id))
    except:
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
                    request.session['active_user'] = {'username' : user.username, 'password' : user.password, 'is_active': user.is_active}
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
    
    except:
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