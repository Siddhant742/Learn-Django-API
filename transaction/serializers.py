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
    
    class Meta:
        model = Order
        fields = ['id', 'prescription', 'total_amount', 'status', 'delivery_address', 'created_at']
        read_only_fields = ['status', 'id', 'created_at']