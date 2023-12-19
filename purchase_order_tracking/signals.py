from django.dispatch import receiver
from django.db.models.signals import post_save, post_init
from .models import PurchaseOrder
from .enums import COMPLETED, CANCELED, PENDING
from .service import update_delivery_rate, update_rating_average, update_fullfilment_rate
from vendor_performance_evaluation.service import update_performance, get_vendor_performance
from vendor_performance_evaluation.models import HistoricalPerformance


@receiver(post_init, sender=PurchaseOrder)
def remember_previous_status(sender, instance, **kwargs):
    instance.previous_status = instance.status


@receiver(post_save, sender=PurchaseOrder)
def purchase_order_post_save(sender, instance, created, **kwargs):
    vendor = instance.vendor
    if not get_vendor_performance(vendor):
        HistoricalPerformance.objects.create(vendor=vendor)

    if not created:
        if instance.status != instance.previous_status:
            print('Status Changed')
            print('Current Status-->',instance.status)
            print('Previous Status-->',instance.previous_status)
            if instance.status == COMPLETED:
                update_delivery_rate(vendor,instance)
                update_rating_average(vendor)

            update_fullfilment_rate(vendor)
