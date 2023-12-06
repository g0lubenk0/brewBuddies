from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Group(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User, through='Membership')
    description = models.TextField(default="", null=True, blank=True)
    tags = ArrayField(
        models.CharField(max_length=100)
    )
    place = models.CharField(max_length=250, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    
class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'group']
        
    def __str__(self):
        return f"{self.user.username} in {self.group.name}"