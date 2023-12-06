from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200, null=True)
    desc = models.CharField(max_length=200, null=True)
    profile_img = models.ImageField(default='images/default.png', upload_to='images', null=True, blank=True)
    
    def __str__(self) -> str:
        return self.user.username
    