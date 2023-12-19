
def update_performance(vendor, **kwargs):
    vendor_performance_object = get_vendor_performance(vendor)
    try:
        [setattr(vendor_performance_object,attr,kwargs.get(attr)) for attr in kwargs.keys()]
        vendor_performance_object.save()
    except Exception as e:
        return None

def get_vendor_performance(vendor):
    try:
        return vendor.performance.all().last()
    except Exception as e:
        return None
