from DjangoApp import settings
import hashlib
import urllib.parse
import requests
import urllib.parse
import socket
from werkzeug.urls import url_parse

SALT_PASS_PHRASE = 'jt7NOE43FZPn'
BASE_URL = settings.ALLOWED_HOSTS[1] if settings.DEBUG else settings.ALLOWED_HOSTS[1]
RETURN_URL = f'https://{BASE_URL}/AuctionApp/paymentreturn'
CANCEL_URL = f'https://{BASE_URL}/AuctionApp/paymentcancel'
NOTIFY_URL = f'https://{BASE_URL}/AuctionApp/paymentnotify'
MERCHANT_ID = '10026869'
MERCHANT_KEY = '82keksxoncsoi'
PAYFAST_HOST = 'sandbox.payfast.co.za' if settings.DEBUG else 'www.payfast.co.za'
SEND_CONFIRMATION_EMAIL = '1'

def dataToString(dataArray, passPhrase = ''):
    pfParamString = ""
    for key in dataArray:
        pfParamString += key + "=" + urllib.parse.quote_plus(dataArray[key].replace("+", " ")) + "&"
   
    pfParamString = pfParamString[:-1]
    if passPhrase != '':
        pfParamString += f"&passphrase={passPhrase}"
    return pfParamString

def generateSignature(dataArray, passPhrase = ''):
    payload = dataToString(dataArray, passPhrase)
    return hashlib.md5(payload.encode()).hexdigest()

def get_paysafe_payment_data(user, item):
    user_id = user['id']
    paysafe_payment_data = {
        'merchant_id': MERCHANT_ID,
        'merchant_key': MERCHANT_KEY,
        'return_url': RETURN_URL,
        'cancel_url': CANCEL_URL,
        'notify_url': f'{NOTIFY_URL}/{user_id}/{item.id}',

        'name_first': user['first_name'],
        'name_last': user['last_name'],
        'email_address': user['email'],

        'm_payment_id': f'{item.id}',
        'amount': f'{item.amount}',
        'item_name': f'{item.name}',
        'item_description': f'{item.description}',
        'email_confirmation': SEND_CONFIRMATION_EMAIL
    }

    paysafe_payment_data['signature'] = generateSignature(paysafe_payment_data, SALT_PASS_PHRASE)
    paysafe_payment_data['redirect_to_url'] = 'https://sandbox.payfast.co.za/eng/process' if settings.DEBUG else 'https://www.payfast.co.za/eng/process'

    return paysafe_payment_data

def pfValidSignature(pfData, pfParamString):
  # Generate our signature from PayFast parameters
  signature = hashlib.md5(pfParamString.encode()).hexdigest()
  return (pfData.get('signature') == signature) 

def pfValidIP(request):
    valid_hosts = [
    'www.payfast.co.za',
    'sandbox.payfast.co.za',
    'w1w.payfast.co.za',
    'w2w.payfast.co.za',
    ]
    valid_ips = []

    for item in valid_hosts:
        ips = socket.gethostbyname_ex(item)
        if ips:
            for ip in ips:
                if ip:
                    valid_ips.append(ip)
    # Remove duplicates from array
    clean_valid_ips = []
    for item in valid_ips:
        # Iterate through each variable to create one list
        if isinstance(item, list):
            for prop in item:
                if prop not in clean_valid_ips:
                    clean_valid_ips.append(prop)
        else:
            if item not in clean_valid_ips:
                clean_valid_ips.append(item)

    # Security Step 3, check if referrer is valid
    if url_parse(request.headers.get("Referer")).host not in clean_valid_ips:
        return False
    else:
        return True

def pfValidPaymentData(cartTotal, pfData):
    return not (abs(float(cartTotal)) - float(pfData.get('amount_gross'))) > 0.01

def pfValidServerConfirmation(pfParamString, pfHost = 'sandbox.payfast.co.za'):
    url = f"https://{pfHost}/eng/query/validate"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
    response = requests.post(url, data=pfParamString, headers=headers)
    return response.text == 'VALID'

def is_payfast_payment_successful(request, amount):
    pfData = request.POST
    pfParamString = ""

    for key in pfData:
        if key != 'signature':
            pfParamString += key + "=" + urllib.parse.quote_plus(pfData[key].replace("+", " ")) + "&"
    pfParamString += f"passphrase={SALT_PASS_PHRASE}"
    
    check1 = pfValidSignature(pfData, pfParamString, )
    check2 = pfValidIP(request)
    check3 = pfValidPaymentData(amount, pfData)
    check4 = pfValidServerConfirmation(pfParamString, PAYFAST_HOST)

    return check1 and check2 and check3 and check4






