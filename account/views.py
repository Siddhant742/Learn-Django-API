from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db import IntegrityError
from .serializers import UserRegistrationSerializer, UserLoginSerializer

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    },
                    'message': 'User registered successfully.'
                }, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                if 'UNIQUE constraint failed: auth_user.username' in str(e):
                    return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                elif 'UNIQUE constraint failed: auth_user.email' in str(e):
                    return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'An error occurred during registration.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)