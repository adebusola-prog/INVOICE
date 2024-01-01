from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Customer, Invoice, InvoiceItem
from .forms import CustomerForm, InvoiceItemFormSet
from django.views.generic.edit import CreateView


class CustomerCreateView(View):
    template_name = 'invoice/customer_create.html'

    def get(self, request):
        form = CustomerForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            return redirect('invoice/customer_detail', pk=customer.pk)
        return render(request, self.template_name, {'form': form})


class CustomerListView(View):
    template_name = 'invoice/customer_list.html'

    def get(self, request):
        customers = Customer.active_objects.all()
        return render(request, self.template_name, {'customers': customers})


class CustomerDetailView(View):
    template_name = 'invoice/customer_detail.html'

    def get(self, request, pk):
        customer = Customer.active_objects.get(pk=pk)
        invoices = Invoice.active_objects.filter(customer=customer)
        return render(request, self.template_name, {'customer': customer, 'invoices': invoices})


class CustomerInvoicesView(View):
    template_name = 'invoice/customer_invoice.html'

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(pk=self.kwargs['pk'])
        invoices = Invoice.objects.filter(customer=customer)
        context = {'customer': customer, 'invoices': invoices}
        return render(request, self.template_name, context)
    

class InvoiceCreateView(View):
    template_name = 'invoice/invoice_create.html'

    def get(self, request, pk):
        customer = Customer.active_objects.get(pk=pk)
        formset = InvoiceItemFormSet(queryset=InvoiceItem.objects.none())
        return render(request, self.template_name, {'customer': customer, 'formset': formset})

    def post(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        formset = InvoiceItemFormSet(request.POST)
        if formset.is_valid():
            deposit = request.POST.get('deposit', 0)
            deposit2 = request.POST.get('deposit2', 0)
            invoice = Invoice.objects.create(customer=customer, deposit=deposit, deposit2=deposit2)
            for form in formset:
                if form.cleaned_data:
                    item = form.save(commit=False)
                    item.invoice = invoice
                    item.save()
            return redirect('customer_detail', pk=pk)
        return render(request, self.template_name, {'customer': customer, 'formset': formset})
    

class InvoiceListView(View):
    template_name = 'invoice/invoice_list.html'

    def get(self, request):
        invoices = Invoice.objects.all()
        return render(request, self.template_name, {'invoices': invoices})


class InvoiceDetailView(View):
    template_name = 'invoice/invoice_detail.html'

    def get(self, request, invoice_id):
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        invoice_items = InvoiceItem.objects.filter(invoice=invoice)
        return render(request, self.template_name, {'invoice': invoice, 'invoice_items': invoice_items})

