from django.shortcuts import render
from rest_framework import viewsets, response, status
from .serializers import PurchaseOrderSerializer
from .models import PurchaseOrder
from .service import update_purchase_orders, update_average_response_time
from vendor_performance_evaluation.service import update_performance
from VMS.auth import AuthBaseViewSet


class PurchaseOrderViewset(viewsets.ModelViewSet, AuthBaseViewSet):
    serializer_class = PurchaseOrderSerializer
    queryset = PurchaseOrder.objects.all()

    def list(self, request, po_id=None):
        try:
            if po_id:
                instance = self.queryset.filter(id=po_id).last()
                if instance:
                    return response.Response(self.serializer_class(instance=instance).data)
                else:
                    return response.Response(f"Purchase Order with this ID not Found {po_id}")
            if request.query_params.get('vendor_code'):
                self.queryset = self.queryset.filter(vendor__vendor_code=request.query_params.get('vendor_code'))
                return super(PurchaseOrderViewset, self).list(request)
            else:
                return super(PurchaseOrderViewset, self).list(request)

        except Exception as e:
            return response.Response(f'Error Occured {str(e)}', status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        try:

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return response.Response(serializer.data,
                                         status=status.HTTP_200_OK)
            else:
                return response.Response("Order Not Created", status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return response.Response(f'Error Occured {str(e)}', status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:

            instance = self.get_object()
            if instance:
                serializer = self.serializer_class(instance, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save(**serializer.validated_data)
                    return response.Response(serializer.data, status=status.HTTP_200_OK)
                return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return response.Response('No Vendor Exists', status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return response.Response(f'Error Occured {str(e)}', status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, instance, pk):
        try:
            instance = self.get_object()
            if instance:
                self.perform_destroy(instance)
                return response.Response('Deletion Complete')
            else:
                return response.Response('Vendor Doesnt Exist', status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return response.Response(f'Error Occured {str(e)}', status=status.HTTP_404_NOT_FOUND)


class POAcknowledgmentViewset(viewsets.ModelViewSet, AuthBaseViewSet):
    serializer_class = PurchaseOrderSerializer
    queryset = PurchaseOrder.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            purchase_object = PurchaseOrder.objects.filter(id=kwargs.get('po_id')).last()
            if purchase_object:
                update_purchase_orders(purchase_object,
                                       **{'acknowledgement_date': request.data.get('acknowledgement_date')})
                vendor_obj = purchase_object.vendor
                update_average_response_time(vendor_obj)
                return response.Response(self.serializer_class(purchase_object).data)

            else:
                return response.Response({'Error Message': 'Purchase object Not Found'},
                                         status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
