from django.contrib import admin
from .models import PurchaseOrder


# Register your models here.

class PurchaseOrderAdmin(admin.ModelAdmin):
    model = PurchaseOrder
    list_display = ['po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity',
                    'status', 'quality_rating', 'issue_date', 'acknowledgement_date']


admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
