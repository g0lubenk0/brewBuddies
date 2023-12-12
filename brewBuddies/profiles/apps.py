from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """
    Django AppConfig for Profiles

    This AppConfig class, `ProfilesConfig`, is part of a Django app named 'profiles'. It provides configuration settings for the 'profiles' app, including specifying the default auto field and defining the `ready` method to handle any initialization logic, such as connecting signals.

    Attributes:
        default_auto_field (str): Specifies the default auto field for models in the 'profiles' app. It is set to 'django.db.models.BigAutoField', indicating the use of the Big Auto Field for primary keys.
        name (str): The name of the 'profiles' app.

    Methods:
        ready(self): This method is automatically called when the Django application is loaded. It is used to perform any initialization logic or setup tasks for the 'profiles' app. In this case, it imports and connects signals from the 'profiles.signals' module.

    Usage:
        This AppConfig is typically defined in the 'apps.py' file of the 'profiles' app. To activate this configuration, it should be specified in the 'INSTALLED_APPS' list in the Django project's settings.

    Example:
    # In the 'apps.py' file of the 'profiles' app
    from django.apps import AppConfig

    class ProfilesConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'profiles'

        def ready(self):
            import profiles.signals
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        import profiles.signals