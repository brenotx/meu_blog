from datetime import date
from django import forms
from django.forms.extras.widgets import SelectDateWidget

from .models import BillPay, BillReceive


class PaymentForm(forms.Form):
    value = forms.DecimalField(max_digits=15, decimal_places=2)


def save_payment(self, bill):
    return bill.trow_payment(
        payment_date=date.today(),
        value=self.cleaned_date['value']
    )


class BillPayForm(forms.ModelForm):
    class Meta:
        model = BillPay
        exclude = ('user', 'operation', 'payment_date',)

    def __init__(self, *args, **kwargs):
        self.base_fields['expiration_date'].widget = SelectDateWidget()

        super(BillPayForm, self).__init__(*args, **kwargs)


class BillReceiveForm(forms.ModelForm):
    class Meta:
        model = BillReceive
        exclude = ('user', 'operation', 'payment_date',)

    def __init__(self, *args, **kwargs):
        self.base_fields['expiration_date'].widget = SelectDateWidget()

        super(BillReceiveForm, self).__init__(*args, **kwargs)
