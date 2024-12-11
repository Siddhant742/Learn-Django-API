from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Prescription, Order
from .serializers import PrescriptionSerializer, OrderSerializer

class PrescriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        return Prescription.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['GET'])
    def order_status(self, request, pk=None):
        try:
            prescription = self.get_object()
            order = Order.objects.filter(prescription=prescription).first()
            if not order:
                return Response({
                    'message': 'No associated order found.'
                }, status=status.HTTP_404_NOT_FOUND)
            return Response({
                'order_status': order.status
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'An error occurred while fetching order status.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).select_related('prescription').order_by('-created_at')

    def perform_create(self, serializer):
        prescription_image = self.request.data.get('prescription_image')
        latitude = self.request.data.get('latitude')
        longitude = self.request.data.get('longitude')
        serializer.save(prescription_image=prescription_image, latitude=latitude, longitude=longitude)
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import Prescription, Order
# from .serializers import PrescriptionSerializer, OrderSerializer

# class PrescriptionViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PrescriptionSerializer

#     def get_queryset(self):
#         return Prescription.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     @action(detail=True, methods=['GET'])
#     def order_status(self, request, pk=None):
#         try:
#             prescription = self.get_object()
#             order = Order.objects.filter(prescription=prescription).first()
            
#             if not order:
#                 return Response({
#                     'message': 'No associated order found.'
#                 }, status=status.HTTP_404_NOT_FOUND)

#             return Response({
#                 'order_status': order.status
#             }, status=status.HTTP_200_OK)
        
#         except Exception as e:
#             return Response({
#                 'error': 'An error occurred while fetching order status.',
#                 'details': str(e)
#             }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class OrderViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = OrderSerializer

#     def get_queryset(self):
#         return Order.objects.filter(
#             user=self.request.user
#         ).select_related('prescription').order_by('-created_at')

#     def perform_create(self, serializer):
#         prescription_image = self.request.data.get('prescription_image')
#         prescription_data = {'prescription_image': prescription_image} if prescription_image else None
        
#         serializer.save(
#             user=self.request.user,
#             prescription_data=prescription_data
#         )

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response({
#             'id': serializer.data['id'],
#             'prescription': serializer.data['prescription'],
#             'status': serializer.data['status'],
#             'delivery_address': serializer.data['delivery_address'],
#             'created_at': serializer.data['created_at'],
#             'payment_slip': serializer.data['payment_slip']
#         })