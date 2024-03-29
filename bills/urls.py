from django.conf.urls import patterns, url

from .models import BillPay, BillReceive
from .forms import BillPayForm, BillReceiveForm


urlpatterns = patterns('bills.views',
    url(r'^$', 'bills', name='bills-bills'),
    url(r'^pay/(?P<bill_id>\d+)/$', 'bill',
        {'classe': BillPay},
        name='bill_to_pay'),
    url(r'^receive/(?P<bill_id>\d+)/$', 'bill',
        {'classe': BillReceive},
        name='bill_to_receive'),
    url(r'^pay/(?P<bill_id>\d+)/pay/$', 'bill_payment',
        {'classe': BillPay},
        name="bill_to_pay_payment"),
    url(r'^receive/(?P<bill_id>\d+)/pay/$', 'bill_payment',
        {'classe': BillReceive},
        name="bill_to_receive_payment"),
    url(r'^pay/$', 'bills_per_classe',
        {'classe': BillPay, 'titulo': 'Contas a Pagar'},
        name='bills_to_pay'),
    url(r'^receive/$', 'bills_per_classe',
        {'classe': BillReceive, 'titulo': 'Contas a Receber'},
        name='bills_to_receive'),
    url(r'^pay/new/$', 'edit_bill',
        {'classe_form': BillPayForm, 'titulo': 'Conta a Pagar'},
        name='new_bill_to_pay'),
    url(r'^receive/new/$', 'edit_bill',
        {'classe_form': BillReceiveForm, 'titulo': 'Conta a Receber'},
        name='new_bill_to_receive'),
    url(r'^pay/(?P<bill_id>\d+)/edit/$', 'edit_bill',
        {'classe_form': BillPayForm, 'titulo': 'Conta a Pagar'},
        name='edit_bill_to_pay'),
    url(r'^receive/(?P<bill_id>\d+)/edit/$', 'edit_bill',
        {'classe_form': BillReceiveForm, 'titulo': 'Conta a Receber'},
        name='edit_bill_to_receive'),
    url(r'^pay/(?P<bill_id>\d+)/delete/$', 'delete_bill',
        {'classe': BillPay, 'next': '/bills/pay/'},
        name='delete_bill_to_pay'),
    url(r'^receive/(?P<bill_id>\d+)/delete/$', 'delete_bill',
        {'classe': BillReceive, 'next': '/bills/receive/'},
        name='delete_bill_receive'),
)
