from django.conf.urls import patterns, url

from models import BillPay, BillReceive


urlpatterns = patterns('bills.views',
    url(r'^$', 'bills', name='bills-bills'),
    url(r'^pay/(?P<bill_id>\d+)$', 'bill', {'classe': BillPay}, name='bills-pay'),
    url(r'^receive/(?P<bill_id>\d+)$', 'bill', {'classe': BillReceive}, name='bill-receive'),
    url(r'^pay/(?P<bill_id>\d+)/pay/$', 'bill_payment', {'classe': BillPay}, name="bill_to_pay"),
    url(r'^receive/(?P<bill_id>\d+)/pay/$', 'bill_payment', {'classe':BillReceive}, name="bill_to_receive"),
    url(r'^pay/$', 'bills_per_classe',
        {'classe': BillPay, 'titulo': 'Contas a Pagar'},
        name='bills_to_pay'),
    url(r'^receive/$', 'bills_per_classe',
        {'classe': BillReceive, 'titulo': 'Contas a Receber'},
        name='bills_to_receive'),
)
