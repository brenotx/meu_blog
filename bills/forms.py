from datetime import date
from django import forms


class PaymentForm(forms.Form):
    value = forms.DecimalField(max_digits=15, decimal_places=2)

def save_payment(self, bill):
    return bill.trow_payment(
        payment_date=date.today(),
        value=self.cleaned_date['value']
    )
