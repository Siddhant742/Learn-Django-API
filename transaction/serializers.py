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
    prescription_image = serializers.ImageField(write_only=True)
    description = serializers.CharField(write_only=True, required=False)
    payment_slip = serializers.ImageField(write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'prescription_image', 'status', 'delivery_address', 'description','payment_slip', 'created_at', 'updated_at']

    def create(self, validated_data):
        prescription_image = validated_data.pop('prescription_image')
        prescription = Prescription.objects.create(user=validated_data['user'], prescription_image=prescription_image)
        order = Order.objects.create(prescription=prescription, **validated_data)
        return order