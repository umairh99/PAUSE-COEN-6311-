from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    phone = models.CharField(max_length=15)
    dob = models.DateField(default='2000-01-01')

    def __str__(self):
        return self.user.username
