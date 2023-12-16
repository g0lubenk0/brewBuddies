from django.db import models
from django.contrib.auth.models import User


class ProfileManager(models.Manager):
    def search(self, query):
        return self.filter(models.Q(user__username__icontains=query) |
                           models.Q(name__icontains=query) |
                           models.Q(title__icontains=query) |
                           models.Q(desc__icontains=query))
# Create your models here.

class Profile(models.Model):
    """
    Model representing user profiles.

    Each user can have a corresponding profile containing additional information
    such as name, title, description, and a profile image.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the built-in User model,
            ensuring that each profile is associated with a single user. 
            The on_delete=models.CASCADE parameter specifies that when a user is deleted,
            their associated profile should also be deleted.
        
        name (CharField): A field to store the name of the user. 
            It has a maximum length of 200 characters and can be null.
        
        title (CharField): A field to store the title or role of the user. 
            It has a maximum length of 200 characters and can be null.
        
        desc (CharField): A field to store a short description or bio of the user. 
            It has a maximum length of 200 characters and can be null.
        
        profile_img (ImageField): A field to store the user's profile image. 
            It has a default value pointing to a default image if no image is provided.
            Images are uploaded to the 'images' directory. 
            This field can be null and is marked as blank to allow empty values.

    Methods:
        __str__: A method that returns a string representation of the profile. 
            It returns the username of the associated user.

    Usage:
        To use this model, include it in your Django app's models and run migrations 
        to create the corresponding database table.

    Dependencies:
        - Django: This model depends on the Django framework, specifically the 
          built-in models and User class.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200, null=True)
    desc = models.CharField(max_length=200, null=True)
    profile_img = models.ImageField(default='images/default.png', upload_to='images', null=True, blank=True)
    
    objects = ProfileManager()
    
    def __str__(self) -> str:
        return self.user.username
    