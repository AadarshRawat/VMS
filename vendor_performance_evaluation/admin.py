from django.contrib import admin
from .models import HistoricalPerformance


# Register your models here.

class HistoricalPerformanceAdmin(admin.ModelAdmin):
    model = HistoricalPerformance
    list_display = ['vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time',
                    'fulfillment_rate']


admin.site.register(HistoricalPerformance, HistoricalPerformanceAdmin)
