from django import forms
from .models import Customer, InvoiceItem, NigerianPhoneNumberField, Invoice


class CustomerForm(forms.ModelForm):
    phone_number = NigerianPhoneNumberField() 

    class Meta:
        model = Customer
        fields = ['name', 'address', 'phone_number']


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['quantity', 'goods_description', 'rate']

InvoiceItemFormSet = forms.modelformset_factory(InvoiceItem, form=InvoiceItemForm, extra=1)
        
