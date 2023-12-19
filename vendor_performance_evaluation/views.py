from django.shortcuts import render
from rest_framework import viewsets, response, status
from .serializers import HistoricalPerformanceSerializer
from .models import HistoricalPerformance
from VMS.auth import AuthBaseViewSet


class HistoricalPerformanceViewset(viewsets.ModelViewSet, AuthBaseViewSet):
    serializer_class = HistoricalPerformanceSerializer
    queryset = HistoricalPerformance.objects.all()

    def list(self, request, id):
        try:
            self.queryset = self.queryset.filter(vendor__id=id)
            return super(HistoricalPerformanceViewset, self).list(request)
        except Exception as e:
            return response.Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
