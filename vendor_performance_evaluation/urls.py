from django.urls import path, include
from vendor_performance_evaluation.views import HistoricalPerformanceViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', HistoricalPerformanceViewset, basename='vendor')

urlpatterns = router.urls
