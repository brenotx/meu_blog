from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator 

from models import BillPay, BillReceive, BILL_STATUS_PAYABLE
from forms import PaymentForm


def bills(request):
    bills_to_pay = BillPay.objects.filter(
        status=BILL_STATUS_PAYABLE,
    )
    bills_to_receive = BillReceive.objects.filter(
        status=BILL_STATUS_PAYABLE,
    )

    return render_to_response(
        'bills/bills.html',
        locals(),
        context_instance=RequestContext(request),
    )

def bill(request, bill_id, classe):
    bill = get_object_or_404(classe, id=bill_id)
    payment_form = PaymentForm()
    
    return render_to_response(
        'bills/bill.html',
        locals(),
        context_instance=RequestContext(request),

    )

def bill_payment(request, bill_id, classe):
    bill = get_object_or_404(classe, id=bill_id)

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)

        if payment_form.is_valid():
            payment_form.save_payment(bill)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def bills_per_classe(request, classe, titulo):
    bills = classe.objects.order_by('status', 'expiration_date')
    paginacao = Paginator(bills, 5)
    pagina = paginacao.page(request.GET.get('pagina', 1))
    titulo = _(titulo)
    return render_to_response(
        'bills/bills_per_classe.html',
        locals(),
        context_instance=RequestContext(request),
    )
