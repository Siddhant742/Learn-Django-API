from rest_framework import serializers
from .models import Prescription, Order
from django.core.validators import FileExtensionValidator

class PrescriptionSerializer(serializers.ModelSerializer):
    prescription_image = serializers.ImageField(
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'pdf'])],
        required=True
    )

    class Meta:
        model = Prescription
        fields = ['id', 'prescription_image', 'status', 'created_at']
        read_only_fields = ['status', 'id', 'created_at']

    def validate(self, data):
        max_file_size = 10 * 1024 * 1024  # 10MB
        if data.get('prescription_image'):
            if data['prescription_image'].size > max_file_size:
                raise serializers.ValidationError({
                    'prescription_image': "Prescription file size must be under 10MB."
                })
        return data

class OrderSerializer(serializers.ModelSerializer):
    prescription = PrescriptionSerializer(read_only=True)
    payment_slip = serializers.ImageField(required=True)
    delivery_address = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'prescription', 'status', 'delivery_address', 
                 'payment_slip', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_payment_slip(self, value):
        max_file_size = 10 * 1024 * 1024  # 10MB
        if value.size > max_file_size:
            raise serializers.ValidationError(
                "Payment slip file size must be under 10MB."
            )
        return value

    def create(self, validated_data):
        user = validated_data.pop('user')
        prescription_data = validated_data.pop('prescription_data', None)
        
        if prescription_data and prescription_data.get('prescription_image'):
            prescription = Prescription.objects.create(
                user=user,
                prescription_image=prescription_data['prescription_image']
            )
        else:
            raise serializers.ValidationError({
                'prescription': "Prescription data is required."
            })
            
        order = Order.objects.create(
            user=user,
            prescription=prescription,
            **validated_data
        )
        return order

