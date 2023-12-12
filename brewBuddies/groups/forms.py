from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    """ 
    Django Form for Group Model

    This module defines a Django Form for the Group model. It utilizes the ModelForm class provided by Django's forms module to simplify the creation of forms that directly correspond to a model.

    The GroupForm allows users to input information related to the Group model, including fields such as name, description, tags, place, latitude, and longitude.

    Usage:
    1. Import the GroupForm in your views or wherever form handling is required.
    2. Instantiate the form and use it in your Django views or templates.

    Example:
    ```python
    from django import forms
    from .models import Group

    class MyView(View):
        def get(self, request):
            # Instantiate the GroupForm
            group_form = GroupForm()
            return render(request, 'my_template.html', {'group_form': group_form})
    ```

    Attributes:
    - `model` (Group): The Django model associated with this form.
    - `fields` (List): The list of fields from the associated model that will be included in the form.

    Note:
    - This form assumes that the corresponding model (Group) is defined and imported from the same application.

    See Also:
    - Django ModelForm: https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/

    """
    class Meta:
        model = Group
        fields = ['name', 'description', 'tags', 'place', 'latitude', 'longitude']
