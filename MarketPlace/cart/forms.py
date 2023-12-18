from django import forms
from django.contrib import admin
from .models import Invoice

class InvoiceAdminForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceAdmin(admin.ModelAdmin):
    form = InvoiceAdminForm

