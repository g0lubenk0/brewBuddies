from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    """
    Model representing a group.

    Each group has a name, description, tags, creator, members, place, latitude, and longitude.

    Attributes:
        name (CharField): The name of the group.
        description (TextField): A detailed description of the group (default is 'some desc').
        tags (CharField): Tags or keywords associated with the group.
        creator (ForeignKey): A foreign key referencing the User who created the group.
        members (ManyToManyField): Many-to-many relationship with User, representing members of the group.
        place (CharField): The location or place associated with the group (default is 'Moscow').
        latitude (FloatField): The latitude coordinate of the group's location (default is 55.755735).
        longitude (FloatField): The longitude coordinate of the group's location (default is 37.620996).

    Methods:
        __str__(): Returns the string representation of the group, which is its name.

    Example:
        group = Group(name='Sample Group', description='Sample description', tags='sample, group',
                      creator=user_instance, place='New York', latitude=40.7128, longitude=-74.0060)
        group.save()

    """
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