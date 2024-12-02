from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    def __str__(self):
        return self.username
# Compare this snippet from learnDjango/account/urls.py: