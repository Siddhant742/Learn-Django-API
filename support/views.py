from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import FAQ, TermsAndConditions, PrivacyPolicy, ContactMessage
from .serializers import (
    FAQSerializer, 
    TermsAndConditionsSerializer, 
    PrivacyPolicySerializer, 
    ContactMessageSerializer
)

class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.all().order_by('order')
    serializer_class = FAQSerializer

class SupportDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    def list(self, request):
        try:
            terms = TermsAndConditions.objects.first()
            privacy = PrivacyPolicy.objects.first()

            return Response({
                'terms_and_conditions': TermsAndConditionsSerializer(terms).data,
                'privacy_policy': PrivacyPolicySerializer(privacy).data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'error': 'An error occurred while fetching support documents.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContactMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ContactMessageSerializer

    def create(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'message': 'Thank you for your message. We will get back to you soon.'
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                'error': 'An error occurred while submitting your message.',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)