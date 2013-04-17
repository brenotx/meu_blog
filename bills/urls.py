from django.conf.urls import patterns, url, include

from models import BillPay, BillReceive


urlpatterns = patterns('bills.views',
    url(r'^$', 'bills', name='bills-bills'),
    url(r'^pay/(?P<bill_id>\d+)$', 'bill', {'classe': BillPay}, name='bills-pay'),
    url(r'^receive/(?P<bill_id>\d+)$', 'bill', {'classe': BillReceive}, name='bill-receive')
)
