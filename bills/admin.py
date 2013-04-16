from django.contrib import admin

from models import Person, History, Bill, BillPay, BillReceive, PaymentPaid, PaymentReceived


class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone',)

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('description',)

class BillAdmin(admin.ModelAdmin):
    list_display = ('expiration_date', 'value', 'status', 'operation', 'history', 'person',)
    search_fields = ('description',)
    list_filter = ('expiration_date', 'status', 'operation', 'history', 'person',)

class InlinePaymentPaid(admin.TabularInline):
    model = PaymentPaid

class BillPayAdmin(admin.ModelAdmin):
    list_display = ('expiration_date', 'value', 'status', 'history', 'person',)
    search_fields = ('description',)
    list_filter = ('expiration_date', 'status', 'history', 'person',)
    exclude = ['operation',]
    inlines = [InlinePaymentPaid,]

class InlinePaymentReceived(admin.TabularInline):
    model = PaymentReceived

class BillReceiveAdmin(admin.ModelAdmin):
    list_display = ('expiration_date', 'value', 'status', 'history', 'person',)
    search_fields = ('description',)
    list_filter = ('expiration_date', 'status', 'history', 'person',)
    exclude = ['operation',]
    inlines = [InlinePaymentReceived,]
    date_hierarchy = 'expiration_date'

admin.site.register(Person, PersonAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(BillPay, BillPayAdmin)
admin.site.register(BillReceive, BillReceiveAdmin)

