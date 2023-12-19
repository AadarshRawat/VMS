from django.shortcuts import render
from rest_framework import viewsets, response, status
from .serializers import VendorSerializer
from .models import Vendor
from VMS.auth import AuthBaseViewSet


class VendorDetailsViewset(viewsets.ModelViewSet, AuthBaseViewSet):
    serializer_class = VendorSerializer
    queryset = Vendor.objects.all()

    def list(self, request):
        try:
            return super(VendorDetailsViewset, self).list(request)
        except Exception as e:
            return response.Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:

            instance = self.queryset.filter(id=kwargs.get('pk')).last()
            return response.Response(self.serializer_class(instance=instance).data)

        except Exception as e:
            return response.Response({'Error': e}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        try:

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return response.Response(serializer.data,
                                         status=status.HTTP_200_OK)
            else:
                return response.Response(common_error_message_format_for_client(error_message="Vendor Not Created",
                                                                                code=500), status=500)
        except Exception as e:
            return response.Response({'Error': e}, status=status.HTTP_400_BAD_REQUEST)

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
                return response.Response(
                    common_error_message_format_for_client(f"No Vendor Exists with id {kwargs.get('pk')}", 400),
                    status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return response.Response({'Error': e}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, instance, pk):
        try:

            instance = self.get_object()
            if instance:
                self.perform_destroy(instance)
                return response.Response('Deletion Complete')
            else:
                return response.Response('Vendor Doesnt Exist')

        except Exception as e:
            return response.Response({'Error': e}, status=status.HTTP_400_BAD_REQUEST)
