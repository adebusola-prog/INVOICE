from django.db import models
from django.core.validators import RegexValidator
from django.utils.functional import cached_property
from phonenumber_field.modelfields import PhoneNumberField
from base.models import  BaseModel


class NigerianPhoneNumberField(PhoneNumberField):
    default_validators = [
        RegexValidator(
            r"^(?:\+?234|0)[789]\d{9}$",
            message="Please enter a valid Nigerian phone number starting with +234.",
            code="invalid_phone_number",
        ),
    ]

    def formfield(self, **kwargs):
        defaults = {
            "validators": self.default_validators,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)
    

class Customer(BaseModel):
    name = models.CharField(max_length=300)
    address = models.TextField()
    phone_number = models.JSONField()
    invoice = models.ForeignKey('Invoice', on_delete=models.SET_NULL, null=True,
                                 blank=True, related_name="customers")

    def __str__(self):
        return self.name


class Invoice(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    date = models.DateTimeField(auto_now_add=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposit2 = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.customer.name
    
    @cached_property
    def total_amount(self):
        return sum(item.amount for item in self.items.all())

    @cached_property
    def balance(self):
        return self.total_amount - (self.deposit + self.deposit2)


class InvoiceItem(BaseModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField()
    goods_description = models.CharField(max_length=50)
    rate =  models.DecimalField(max_digits=10, decimal_places=2)
    
    
    def __str__(self):
        return self.invoice.customer.name

    @cached_property
    def amount(self):
        return self.quantity * self.rate