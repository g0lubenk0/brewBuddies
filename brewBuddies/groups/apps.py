from django.apps import AppConfig


class GroupsConfig(AppConfig):
    """
    Django App Configuration for 'groups'

    This module defines the configuration for the 'groups' app within a Django project. It extends the base AppConfig class provided by Django to customize the app's behavior.

    Attributes:
        default_auto_field (str): The default primary key field type for models in this app. It is set to 'django.db.models.BigAutoField', indicating the use of a large auto-incrementing integer field as the default primary key.
        
        name (str): The name of the app, which is set to 'groups'. This is used to uniquely identify the app within the Django project.

    Example:
        ```python
        # In your Django project's settings.py, you might have:
        INSTALLED_APPS = [
            # ...
            'groups',
            # ...
        ]
        ```

    This configuration allows Django to recognize and manage the 'groups' app within the project.

    For more information on AppConfig, see:
    https://docs.djangoproject.com/en/3.2/ref/applications/#configuring-applications
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'groups'
