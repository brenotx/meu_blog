import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator
from django.contrib import messages

from .models import BillPay, BillReceive, BILL_STATUS_PAYABLE
from .forms import PaymentForm


def bills(request):
    bills_to_pay = BillPay.objects.filter(
        status=BILL_STATUS_PAYABLE,)
    bills_to_receive = BillReceive.objects.filter(
        status=BILL_STATUS_PAYABLE,)

    return render_to_response(
        'bills/bills.html',
        locals(),
        context_instance=RequestContext(request),)


def bill(request, bill_id, classe):
    bill = get_object_or_404(classe, id=bill_id)
    payment_form = PaymentForm()

    return render_to_response(
        'bills/bill.html',
        locals(),
        context_instance=RequestContext(request),)


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
        context_instance=RequestContext(request),)


def edit_bill(request, classe_form, titulo, bill_id=None):
    if bill_id:
        bill = get_object_or_404(classe_form._meta.model, id=bill_id)
    else:
        bill = None

    if request.method == 'POST':
        form = classe_form(request.POST, instance=bill)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.user = request.user
            bill.save()

            return HttpResponseRedirect(bill.get_absolute_url())
    else:
        form = classe_form(initial={'expiration_date': datetime.date.today()},
                                    instance=bill,)

    return render_to_response('bills/edit_bill.html',
                              locals(),
                              context_instance=RequestContext(request),)


def delete_bill(request, classe, bill_id, next='/bills/'):
    bill = get_object_or_404(classe, id=bill_id)
    bill.delete()

    messages.info(request, 'Conta excluida com sucesso!')

    return HttpResponseRedirect(next)
