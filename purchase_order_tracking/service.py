from .enums import COMPLETED, CANCELED, PENDING
from vendor_performance_evaluation.service import update_performance, get_vendor_performance
from datetime import date, datetime, timezone


def update_average_response_time(vendor):
    purchase_orders = get_purchase_orders(vendor)
    total_time = 0
    if len(purchase_orders) > 0:
        for order in purchase_orders:
            time_difference = order.issue_date - order.acknowledgement_date
            total_time += time_difference.total_seconds()
        average_response_time = total_time / len(purchase_orders)
        update_performance(vendor, **{'average_response_time': average_response_time})


def update_delivery_rate(vendor, purchase_order):
    completed_purchase_orders = get_purchase_orders(vendor).filter(status=COMPLETED)
    todays_date = datetime.combine(date.today(), datetime.min.time()).replace(tzinfo=timezone.utc)
    if len(completed_purchase_orders) > 0:
        if len(completed_purchase_orders) == 1:
            if purchase_order.delivery_date <= todays_date:
                on_time_delivery_rate = 1 / len(completed_purchase_orders)
            else:
                on_time_delivery_rate = 0
        else:
            delivery_rate = get_vendor_performance(vendor).on_time_delivery_rate
            successful_purchase_order = delivery_rate * (len(completed_purchase_orders) - 1)
            if purchase_order.delivery_date <= todays_date:
                successful_purchase_order += 1
            on_time_delivery_rate = successful_purchase_order / len(completed_purchase_orders)
        update_performance(vendor, **{'on_time_delivery_rate': on_time_delivery_rate})


def update_rating_average(vendor):
    purchase_orders = get_purchase_orders(vendor)
    total_rating = 0
    if len(purchase_orders) > 0:
        for order in purchase_orders:
            if order.quality_rating:
                total_rating += order.quality_rating

        average_rating = total_rating / len(purchase_orders)
        update_performance(vendor, **{'quality_rating_avg': average_rating})

    else:
        return None


def update_fullfilment_rate(vendor):
    purchase_orders = get_purchase_orders(vendor)
    if len(purchase_orders) > 0:
        sucessfull_pos = 0
        for order in purchase_orders:
            if order.status == COMPLETED:
                sucessfull_pos += 1

        fullfilment_rate = sucessfull_pos / len(purchase_orders)
        update_performance(vendor, **{'fulfillment_rate': fullfilment_rate})
    else:
        return None


def get_purchase_orders(vendor):
    try:
        return vendor.purchase_orders.all()
    except Exception as e:
        return None


def update_purchase_orders(purchase_obj, **kwargs):
    try:
        [setattr(purchase_obj, attr, kwargs.get(attr)) for attr in kwargs.keys()]
        purchase_obj.save()
    except:
        return None
