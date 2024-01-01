from django.urls import path
from .views import (
    CustomerCreateView, 
    CustomerListView,
    CustomerDetailView,
    CustomerInvoicesView, 
    InvoiceCreateView,
    InvoiceListView,
    InvoiceDetailView
    )

app_name = 'invoice'


urlpatterns = [
    path('customer/create', CustomerCreateView.as_view(), name='customer_create'),
    path('customers', CustomerListView.as_view(), name='customer_list'),
    path('customer/<int:pk>', CustomerDetailView.as_view(), name='customer_detail'),
    path('customer/<int:pk>/invoice/create', InvoiceCreateView.as_view(), name='invoice_create'),
    path('customer/invoices', InvoiceListView.as_view(), name='invoice_list'),
    path('customer/invoices/<int:invoice_id>/invoice/', InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoice/customer/invoices/<int:pk>/', CustomerInvoicesView.as_view(), name='customer_invoices'),
]
