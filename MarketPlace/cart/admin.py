from django import forms
from django.contrib import admin
from .models import Invoice

class InvoiceAdminForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceAdmin(admin.ModelAdmin):
    form = InvoiceAdminForm
    list_display = ('id', 'total_price', 'created_at')
    search_fields = ('id', 'total_price', 'created_at')
    list_filter = ('created_at',)

admin.site.register(Invoice, InvoiceAdmin)
