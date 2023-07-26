"""paypal_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from paypal_app.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('add_to_cart/',add_to_cart,name='add_to_cart'),
    path('cart/',cart,name='cart'),
    path('confirm_order/',confirm_order,name='confirm_order'),
    path('payment_data/',payment_data,name='payment_data'),
    path('success/',success,name='success'),
    path('cancel/',cancel,name='cancel'),
    path('req_refund/',req_refund,name='req_refund'),
    path('refund_details/',refund_details),
    path('invoice',invoice),
    path('generate_invoice/',generate_invoice),
    path('send_invoice/',send_invoice,name='send_invoice'),
    path('record_invoice/',record_invoice),
    path('delete_invoice/',delete_invoice,name='delete_invoice'),
    path('cancel_invoice/',cancel_invoice,name='cancel_invoice'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
