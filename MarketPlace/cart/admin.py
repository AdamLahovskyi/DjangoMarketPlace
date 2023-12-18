# admin.py in the cart app
from django import forms
from django.contrib import admin
from .models import Invoice

# Custom form for the Invoice model
class InvoiceAdminForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'

# Custom admin class for the Invoice model
class InvoiceAdmin(admin.ModelAdmin):
    form = InvoiceAdminForm
    # Add other customizations if needed
    list_display = ('id', 'total_price', 'created_at')
    search_fields = ('id', 'total_price', 'created_at')
    list_filter = ('created_at',)

# Register the Invoice model with the custom admin class
admin.site.register(Invoice, InvoiceAdmin)
