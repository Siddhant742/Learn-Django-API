from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    @action(detail=False, methods=['POST'])
    def mark_all_read(self, request):
        try:
            Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
            return Response({
                'message': 'All notifications marked as read.'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'An error occurred while marking notifications.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)