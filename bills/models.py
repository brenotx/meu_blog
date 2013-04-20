# coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class HistoryManager(models.Manager):
    def get_query_set(self):
        query_set = super(HistoryManager, self).get_query_set()

        return query_set.extra(
            select={'_total_value': """select sum(value * case operation when 'c' then 1 else -1 end) from bills_bill where
                                       bills_bill.history_id = bills_history.id""", })


class History(models.Model):
    description = models.CharField(max_length=50)
    user = models.ForeignKey(User)

    objects = HistoryManager()

    def total_value(self):
        return self._total_value or 0

    class Meta:
        ordering = ('description',)

    def __unicode__(self):
        return self.description


class PersonManager(models.Manager):
    def get_query_set(self):
        query_set = super(PersonManager, self).get_query_set()

        return query_set.extra(
            select={
                '_total_value': """select sum(value * case operation when 'c' then 1 else -1 end) from bills_bill
                                where bills_bill.person_id = bills_person.id""",
                '_bills_amount': """select count(value) from bills_bill
                                where bills_bill.person_id = bills_person.id""", })


class Person(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=25, blank=True)
    user = models.ForeignKey(User)

    objects = PersonManager()

    def total_value(self):
        return self._total_value or 0

    def bills_amount(self):
        return self._bills_amount or 0

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

BILL_OPERATION_DEBIT = 'd'
BILL_OPERATION_CREDIT = 'c'
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
    user = models.ForeignKey(User)

    def __unicode__(self):
        date_of_expiration = self.expiration_date.strftime('%d/%m/%Y')
        value = '%0.02f' % self.value

        return '%s - %s (%s)' % (value, self.person.name, date_of_expiration)


class BillPay(Bill):
    def save(self, *args, **kwargs):
        self.operation = BILL_OPERATION_DEBIT
        super(BillPay, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('bill_to_pay', kwargs={'bill_id': self.id})

    def payments(self):
        return self.paymentpaid_set.all()

    def trow_payment(self, payment_date, value):
        return ReceivedPayment.objects.create(bill=self,
                                              payment_date=payment_date,
                                              value=value,)


class BillReceive(Bill):
    def save(self, *args, **kwargs):
        self.operation = BILL_OPERATION_CREDIT
        super(BillReceive, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('bill_to_receive', kwargs={'bill_id': self.id})

    def payments(self):
        return self.paymentreceived_set.all()

    def trow_payment(self, payment_date, value):
        return ReceivedPayment.objects.create(bill=self,
                                              payment_date=payment_date,
                                              value=value,)


class Payment(models.Model):
    payment_date = models.DateField()
    value = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        abstract = True


class PaymentPaid(Payment):
    bill = models.ForeignKey('BillPay')


class PaymentReceived(Payment):
    bill = models.ForeignKey('BillReceive')
