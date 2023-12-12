from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile
from django.forms.models import ModelForm

from django.forms.widgets import FileInput

class CreateUserForm(UserCreationForm):
    """
    A custom form for user registration based on Django's UserCreationForm.

    This form includes fields for username, email, and passwords. It is designed
    to be used in the user registration process.

    Attributes:
    - Meta: A nested class that specifies metadata for the form, including the
      associated User model, fields to include in the form, and their order.

    Usage Example:
    ```python
    form = CreateUserForm(request.POST)
    if form.is_valid():
        # Process the form data
    ```

    """
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
        

class ProfileForm(ModelForm):
    """
    A custom form for updating user profiles based on Django's ModelForm.

    This form is associated with the Profile model and includes fields for
    name, title, description, and a profile image. It excludes the 'user'
    field and customizes the widget for the 'profile_img' field.

    Attributes:
    - Meta: A nested class that specifies metadata for the form, including the
      associated Profile model, fields to include in the form, and their order.
      It also specifies the 'profile_img' field's widget as FileInput.

    Usage Example:
    ```python
    form = ProfileForm(request.POST, request.FILES)
    if form.is_valid():
        # Process the form data
    ```

    """
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'profile_img': FileInput(),
        }
        