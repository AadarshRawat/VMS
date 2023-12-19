from django.urls import path, include
from purchase_order_tracking.views import PurchaseOrderViewset,POAcknowledgmentViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('acknowledge', POAcknowledgmentViewset, basename='acknowledge')
router.register('', PurchaseOrderViewset, basename='purchase_order')


urlpatterns = router.urls
