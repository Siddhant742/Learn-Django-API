from django.db import models
from django.conf import settings

class Prescription(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prescription_image = models.ImageField(upload_to='prescriptions/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Verification'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
#I want a flutter app and custom admin panel in Django to verify the user based on the front and back of ID image. After user is verified, user will be able to order medicine by uploading prescription, address and payment.Admin will verify the prescription and then send the order(when prescription verified, the status should update on the app on API call) User will be able to see the status of order the delivery. User will be able to see the history of orders and prescriptions. User will be able to see the profile and update the profile. User will be able to see the notifications. User will be able to see the FAQ and contact us. User will be able to see the terms and conditions and privacy policy.User will be able to see the logout. User will be able to see the login and signup. User will be able to see the forgot password.User will be able to see the change password.