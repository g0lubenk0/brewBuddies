from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class CustomUser(AbstractUser):
    birthday = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def get_age(self):
        age = date.today() - self.birthday
        return int(age.year)
    
    def __str__(self):
        return self.username
    

class Meetup(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    title = models.CharField(max_length=50, blank=False)
    date = models.DateTimeField(editable=True)
    station = models.CharField(max_length=50, blank=False)
    creator = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="meetup_creator"
    )
    participants = models.ManyToManyField(CustomUser)
    