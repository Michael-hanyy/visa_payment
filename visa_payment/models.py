from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
class SuspiciousLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempts = models.IntegerField(default=0)
    warning_issued = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Attempts: {self.attempts} - Warning: {self.warning_issued}"
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    failed_login_attempts = models.IntegerField(default=0)
    suspicious_warning = models.BooleanField(default=False)
    visa_card_number = models.CharField(max_length=16, blank=True, null=True)
    visa_password = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"