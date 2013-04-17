from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import BillPay, BillReceive, BILL_STATUS_PAYABLE


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
    
    return render_to_response(
        'bills/bill.html',
        locals(),
        context_instance=RequestContext(request),

    )
