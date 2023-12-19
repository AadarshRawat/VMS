from django.urls import path, include
from vendor_profile_management.views import VendorDetailsViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', VendorDetailsViewset, basename='vendor')

urlpatterns = router.urls
