from django.db import models

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

class TermsAndConditions(models.Model):
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

class PrivacyPolicy(models.Model):
    content = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)