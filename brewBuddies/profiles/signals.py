from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

"""
Signals and Receivers for User Profile Creation and Update

This module defines Django signal receivers that automatically create and update user profiles
whenever a new user is created or an existing user is updated.

The signals are connected to the Django `post_save` signal emitted by the `User` model.

Functions:
    - `create_user_profile(sender, instance, created, **kwargs)`: Signal receiver for creating a user profile.
    - `save_user_profile(sender, instance, **kwargs)`: Signal receiver for saving changes to a user profile.

Usage:
    These receivers should be connected to the `post_save` signal of the `User` model.
    When a new user is created, the `create_user_profile` receiver will create a corresponding profile.
    When an existing user is updated, the `save_user_profile` receiver will save changes to the associated profile.

Example:
    # In your signals.py or a similar file:
    from django.db.models.signals import post_save
    from django.dispatch import receiver
    from django.contrib.auth.models import User
    from .models import Profile
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            created = Profile.objects.get_or_create(user=instance)
            
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
"""



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        created = Profile.objects.get_or_create(user=instance)
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()