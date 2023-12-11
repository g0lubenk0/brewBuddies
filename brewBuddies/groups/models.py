from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='some desc')
    tags = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, related_name='joined_groups')
    place = models.CharField(max_length=255, default='Moscow')  # Add place field
    latitude = models.FloatField(max_length=200, default=55.755735)  # Add latitude field
    longitude = models.FloatField(max_length=200, default=37.620996) # Add longitude field

    def __str__(self):
        return self.name