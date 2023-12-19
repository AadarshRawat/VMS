from django.db import models
# Create your models here.
from .enums import STATUS_CHOICES
from vendor_profile_management.models import Vendor


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT,related_name="purchase_orders")
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=30)
    quality_rating = models.FloatField(blank=True, null=True)
    issue_date = models.DateTimeField()
    acknowledgement_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number
