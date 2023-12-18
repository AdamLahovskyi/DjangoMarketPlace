from django.db import models

from item.models import Item

class Invoice(models.Model):
    items = models.ManyToManyField(Item)
    quantities = models.JSONField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_quantities = ', '.join([f'{key}: {value}' for key, value in self.quantities.items()])
        return f"Invoice {self.id} - Quantities: {formatted_quantities}"
