from django.contrib import admin
from .models import Vendor


# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    model = Vendor
    list_display = ['name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate',
                    'quality_rating_avg', 'average_response_time', 'fulfillment_rate']


admin.site.register(Vendor, VendorAdmin)
