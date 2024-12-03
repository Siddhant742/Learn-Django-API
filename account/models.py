from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import FileExtensionValidator, EmailValidator
from django.utils import timezone

class User(models.Model):
    """
    Custom User model without using AbstractUser
    """
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=128)  # Storing hashed password
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Identity verification fields
    is_verified = models.BooleanField(default=False)
    verification_status = models.CharField(
        max_length=20, 
        choices=[
            ('not_submitted', 'Not Submitted'),
            ('pending', 'Pending'),
            ('verified', 'Verified'),
            ('rejected', 'Rejected')
        ],
        default='not_submitted'
    )
    
    # Identity document images
    front_id_image = models.ImageField(
        upload_to='identity_docs/front/', 
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], 
        null=True, 
        blank=True
    )
    back_id_image = models.ImageField(
        upload_to='identity_docs/back/', 
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], 
        null=True, 
        blank=True
    )
    
    # Authentication and account management fields
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    def set_password(self, raw_password):
        """
        Hash and set the password
        """
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Check if the provided password is correct
        """
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

    class Meta:
        app_label = 'account'  # Specify the app label
        verbose_name = 'User'
        verbose_name_plural = 'Users'