from django.shortcuts import render,redirect
from rest_framework.decorators import api_view
import requests
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from .models import Product
import json


def home(request):
    products=Product.objects.all()
    return render(request,'index.html',{'products':products})

def get_token():
    headers = {
            'Content-Type':'application/x-www-form-urlencoded',
        }
    body = {
            'grant_type':'client_credentials'
        }
    r = requests.post("https://api.sandbox.paypal.com/v1/oauth2/token",body, headers, auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET))
    access_token=r.json()['access_token']
    print(access_token)
    return access_token

@api_view(['POST'])
def add_to_cart(request):
    token=get_token()
    
    amount=int(request.POST['amount'])
    quantity=int(request.POST['quantity'])
    amount*=quantity

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token
    }

    url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"

    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "items": [
                    {
                    "name": request.POST['product_name'],
                    "description": request.POST['description'],
                    "quantity": request.POST['quantity'],
                    "unit_amount": {
                    "currency_code": "USD",
                    "value": amount
                        }
                    }
                    ],
                "amount": {
                    "currency_code": "USD",
                    "value": amount,
                    "breakdown": {
                        "item_total": {
                            "currency_code": "USD",
                            "value": amount
                        }
                    }
                }
            }
        ],
        "application_context": {
            "return_url": "http://127.0.0.1:8000/success",
            "cancel_url": "http://127.0.0.1:8000/cancel"
        }
    }
    

    payload=json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    id=response.json()['id']
    return HttpResponseRedirect('/cart/?order_id='+id)

@api_view(['GET'])
def cart(request):
    order_id=request.GET['order_id']
    token=get_token()
    headers = {
    'Authorization': 'Bearer '+token
    }

    response = requests.get('https://api-m.sandbox.paypal.com/v2/checkout/orders/'+order_id, headers=headers)
    return render(request,'cart.html',{'order_id':response.json()['id']})

@api_view(['POST'])
def confirm_order(request):
    token=get_token()
    order_id=request.POST['order_id']
    email=request.POST['email']
    name=request.POST['name']
    sname=request.POST['sname']
    
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+token,
    }

    data = { 
        "payment_source": { 
            "paypal": { 
                "name": { 
                    "given_name": name, 
                    "surname": sname 
                }, 
                "email_address": email, 
                "experience_context": { 
                    "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED", 
                    "payment_method_selected": "PAYPAL", 
                    "brand_name": "EXAMPLE INC", 
                    "locale": "en-US", 
                    "landing_page": "LOGIN", 
                    "shipping_preference": "SET_PROVIDED_ADDRESS", 
                    "user_action": "PAY_NOW", 
                    "return_url": "http://127.0.0.1:8000/success/?order_id="+order_id, 
                    "cancel_url": "http://127.0.0.1:8000/cancel" 
                } 
            } 
        } 
    }
    data=json.dumps(data)
    response = requests.post(f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/confirm-payment-source', headers=headers, data=data)
    return render(request,'payment.html',{'order_id':response.json()['id']})

def success(request):
    order_id=request.GET.get('order_id')
    token=get_token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+token,
    }

    response = requests.post(f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture', headers=headers)
    capture_id = response.json()['purchase_units'][0]['payments']['captures'][0]['id']
    return redirect('/payment_data/?capture_id='+capture_id)

def payment_data(request):
    token=get_token()
    capture_id=request.GET.get('capture_id')
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+token,
    }

    response = requests.get('https://api-m.sandbox.paypal.com/v2/payments/captures/'+capture_id, headers=headers)
    r=response.json()
    context={
        'amount':r['amount']['value'],
        'capture_id':capture_id,
    }
    return render(request,'paymentdata.html',context)


def req_refund(request):
    capture_id=request.POST['capture_id']
    amount=request.POST['amount']
    reason=request.POST['reason']
    token=get_token()
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+token,
    }

    data = {
            "amount":{
                "value":amount,
                "currency_code":"USD"
            },
            "note_to_payer":reason,
            
        }
    data=json.dumps(data)
    response = requests.post(f'https://api-m.sandbox.paypal.com/v2/payments/captures/{capture_id}/refund', headers=headers, data=data)
    refund_id=response.json()['id']
    return redirect('/refund_details/?refund_id='+refund_id)

def refund_details(request):
    token=get_token()
    refund_id=request.GET.get('refund_id')
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+token,
    }

    response = requests.get('https://api-m.sandbox.paypal.com/v2/payments/refunds/'+refund_id, headers=headers)
    return HttpResponse(response.json())

def invoice(request):
    return render(request,'invoice.html')

def generate_invoice(request):
    token=get_token()
    headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json',
    }

    response = requests.post('https://api-m.sandbox.paypal.com/v2/invoicing/generate-next-invoice-number', headers=headers)
    invoice_number=response.json()['invoice_number']
    if invoice_number is not None:
        data=    {
                "detail":{
                    "invoice_number":invoice_number,
                    "reference":"deal-ref",
                    "invoice_date":"2018-11-12",
                    "currency_code":"USD",
                    "note":"Thank you for your business.",
                    "term":"No refunds after 30 days.",
                    "memo":"This is a long contract",
                    "payment_term":{
                        "term_type":"NET_10",
                        "due_date":"2018-11-22"
                    }
                },
                "invoicer":{
                    "name":{
                        "given_name":"David",
                        "surname":"Larusso"
                    },
                    "address":{
                        "address_line_1":"1234 First Street",
                        "address_line_2":"337673 Hillside Court",
                        "admin_area_2":"Anytown",
                        "admin_area_1":"CA",
                        "postal_code":"98765",
                        "country_code":"US"
                    },
                    "email_address":"sb-1zfq726182938@business.example.com",
                    "phones":[
                        {
                            "country_code":"001",
                            "national_number":"4085551234",
                            "phone_type":"MOBILE"
                        }
                    ],
                    "website":"www.test.com",
                    "tax_id":"ABcNkWSfb5ICTt73nD3QON1fnnpgNKBy- Jb5SeuGj185MNNw6g",
                    "logo_url":"https://example.com/logo.PNG",
                    "additional_notes":"2-4"
                },
                "primary_recipients":[
                    {
                        "billing_info":{
                            "name":{
                                "given_name":"Stephanie",
                                "surname":"Meyers"
                            },
                            "address":{
                                "address_line_1":"1234 Main Street",
                                "admin_area_2":"Anytown",
                                "admin_area_1":"CA",
                                "postal_code":"98765",
                                "country_code":"US"
                            },
                            "email_address":"sb-r31ea26376736@personal.example.com",
                            "phones":[
                                {
                                    "country_code":"001",
                                    "national_number":"4884551234",
                                    "phone_type":"HOME"
                                }
                            ],
                            "additional_info_value":"add-info"
                        },
                        "shipping_info":{
                            "name":{
                                "given_name":"Stephanie",
                                "surname":"Meyers"
                            },
                            "address":{
                                "address_line_1":"1234 Main Street",
                                "admin_area_2":"Anytown",
                                "admin_area_1":"CA",
                                "postal_code":"98765",
                                "country_code":"US"
                            }
                        }
                    }
                ],
                "items":[
                    {
                        "name":"Yoga Mat",
                        "description":"Elastic mat to practice yoga.",
                        "quantity":"1",
                        "unit_amount":{
                            "currency_code":"USD",
                            "value":"50.00"
                        },
                        "tax":{
                            "name":"Sales Tax",
                            "percent":"7.25"
                        },
                        "discount":{
                            "percent":"5"
                        },
                        "unit_of_measure":"QUANTITY"
                    },
                    {
                        "name":"Yoga t-shirt",
                        "quantity":"1",
                        "unit_amount":{
                            "currency_code":"USD",
                            "value":"10.00"
                        },
                        "tax":{
                            "name":"Sales Tax",
                            "percent":"7.25"
                        },
                        "discount":{
                            "amount":{
                                "currency_code":"USD",
                                "value":"5.00"
                            }
                        },
                        "unit_of_measure":"QUANTITY"
                    }
                ],
                "configuration":{
                    "partial_payment":{
                        "allow_partial_payment":True,
                        "minimum_amount_due":{
                            "currency_code":"USD",
                            "value":"20.00"
                        }
                    },
                    "allow_tip":True,
                    "tax_calculated_after_discount":True,
                    "tax_inclusive":False,
                },
                "amount":{
                    "breakdown":{
                        "custom":{
                            "label":"Packing Charges",
                            "amount":{
                                "currency_code":"USD",
                                "value":"10.00"
                            }
                        },
                        "shipping":{
                            "amount":{
                                "currency_code":"USD",
                                "value":"10.00"
                            },
                            "tax":{
                                "name":"Sales Tax",
                                "percent":"7.25"
                            }
                        },
                        "discount":{
                            "invoice_discount":{
                                "percent":"5"
                            }
                        }
                    }
                }
            }        
        data=json.dumps(data)
        response = requests.post('https://api-m.sandbox.paypal.com/v2/invoicing/invoices', headers=headers, data=data)
        draft_invoice=response.json()['href']
        if draft_invoice is not None:
            response=requests.get(draft_invoice,headers=headers)
            draft_invoice_id=response.json()['id']
            return render(request,'send_invoice.html',{'draft_invoice':draft_invoice_id})
    
def send_invoice(request):
    token=get_token()
    draft_invoice=request.POST.get('draft_invoice')
    headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json',
    }
   
    response = requests.post(f'https://api-m.sandbox.paypal.com/v2/invoicing/invoices/{draft_invoice}/send', headers=headers)
    context={
        'invoice':draft_invoice,
        'response':response.json()['href']
    }
    return render(request,'makepayment.html',context)

def record_invoice(request):        #this is for partial payment
    token=get_token()
    headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json',
    }

    data = '{ "method": "BANK_TRANSFER", "payment_date": "2023-07-19", "amount": { "currency_code": "USD", "value": "74.00" } }'

    response = requests.post('https://api-m.sandbox.paypal.com/v2/invoicing/invoices/INV2-BZU6-PPBK-QQ9H-T49W/payments', headers=headers, data=data)
    return HttpResponse(response.json())

def delete_invoice(request):
    token=get_token()
    invoice=request.GET['invoice']
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+token,
    }

    response = requests.delete('https://api-m.sandbox.paypal.com/v2/invoicing/invoices/'+invoice, headers=headers)
    return HttpResponse('deleted successfully')

def cancel_invoice(request):
    token=get_token()
    invoice_id=request.GET.get('invoice')
    headers = {
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json',
    }

    data ={
        "subject":"Invoice Cancelled",
        "note":"Cancelling the invoice",
        "send_to_invoicer":True,
        "send_to_recipient":True
    }
    data=json.dumps(data)
    response = requests.post(f'https://api-m.sandbox.paypal.com/v2/invoicing/invoices/{invoice_id}/cancel', headers=headers, data=data)
    return redirect('/delete_invoice/?invoice='+invoice_id)

def cancel(request):
    return HttpResponse('cancelled')