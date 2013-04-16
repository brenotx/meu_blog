# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _


class History(models.Model):
    description = models.CharField(max_length=50)

    class Meta:
        ordering = ('description',)

    def __unicode__(self):
        return self.description

class Person(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=25, blank=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

BILL_OPERATION_DEBIT = 'd'
BILL_OPERATION_CREDIT =  'c'
BILL_OPERATION_CHOICES = (
    (BILL_OPERATION_DEBIT, _('Debito')),
    (BILL_OPERATION_CREDIT, _('Credito')),
)

BILL_STATUS_PAYABLE = 'a'
BILL_STATUS_PAID = 'p'
BILL_STATUS_CHOICES = (
    (BILL_STATUS_PAYABLE, _('A pagar')),
    (BILL_STATUS_PAID, _('Pago')),
)

class Bill(models.Model):
    person = models.ForeignKey('Person')
    history = models.ForeignKey('History')
    expiration_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    operation = models.CharField(
        max_length=1,
        default=BILL_OPERATION_DEBIT,
        choices=BILL_OPERATION_CHOICES,
        blank=True,
    )
    status = models.CharField(
        max_length=1,
        default=BILL_STATUS_PAYABLE,
        choices=BILL_STATUS_CHOICES,
        blank=True,
    )
    description = models.TextField(blank=True)

class BillPay(Bill):
    def save(self, *args, **kwargs):
        self.operation = BILL_OPERATION_DEBIT
        super(BillPay, self).save(*args, **kwargs)

class BillReceive(Bill):
    def save(self, *args, **kwargs):
        self.operation = BILL_OPERATION_CREDIT
        super(BillReceive, self).save(*args, **kwargs)

class Payment(models.Model):
    payment_date = models.DateField()
    value = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        abstract = True

class PaymentPaid(Payment):
    bill = models.ForeignKey('BillPay')

class PaymentReceived(Payment):
    bill = models.ForeignKey('BillReceive')
