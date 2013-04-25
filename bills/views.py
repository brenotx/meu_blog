import datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import BillPay, BillReceive, BILL_STATUS_PAYABLE
from .forms import PaymentForm


@login_required
def bills(request):
    bills_to_pay = BillPay.objects.filter(
        status=BILL_STATUS_PAYABLE, user=request.user,)
    bills_to_receive = BillReceive.objects.filter(
        status=BILL_STATUS_PAYABLE, user=request.user,)

    return render_to_response(
        'bills/bills.html',
        locals(),
        context_instance=RequestContext(request),)


@login_required
def bill(request, bill_id, classe):
    bill = get_object_or_404(classe, id=bill_id)
    if bill.user != request.user:
        raise Http404
    payment_form = PaymentForm()
    return render_to_response(
        'bills/bill.html',
        locals(),
        context_instance=RequestContext(request),)


@login_required
def bill_payment(request, bill_id, classe):
    bill = get_object_or_404(classe, id=bill_id)
    if bill.user != request.user:
        raise Http404
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment_form.save_payment(bill)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def bills_per_classe(request, classe, titulo):
    bills = classe.objects.filter(user=request.user).order_by('status', 'expiration_date')
    paginacao = Paginator(bills, 5)
    pagina = paginacao.page(request.GET.get('pagina', 1))
    titulo = _(titulo)
    return render_to_response(
        'bills/bills_per_classe.html',
        locals(),
        context_instance=RequestContext(request),)


@login_required
def edit_bill(request, classe_form, titulo, bill_id=None):
    if bill_id:
        bill = get_object_or_404(classe_form._meta.model, id=bill_id)
        if bill.user != request.user:
            raise Http404
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


@login_required
def delete_bill(request, classe, bill_id, next='/bills/'):
    bill = get_object_or_404(classe, id=bill_id)
    if bill.user != request.user:
        raise Http404
    bill.delete()

    messages.info(request, 'Conta excluida com sucesso!')

    return HttpResponseRedirect(next)
