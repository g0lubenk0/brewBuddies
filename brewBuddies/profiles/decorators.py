from django.shortcuts import redirect

def unauthenticated_user(view_func):
    """
    Decorator function to redirect authenticated users.

    This decorator is intended to be used with Django views to redirect users who are already authenticated to a specified page, typically the home page.

    Parameters:
    - view_func (function): The original view function that the decorator wraps.

    Returns:
    - function: A wrapper function that checks if the user is authenticated. If the user is authenticated, it redirects them to the 'home' page; otherwise, it allows the original view function to proceed.

    Example:
    ```python
    from django.shortcuts import render
    from django.contrib.auth.decorators import login_required
    from .decorators import unauthenticated_user

    @unauthenticated_user
    def login_view(request):
        # Your view logic for the login page
        return render(request, 'login.html')
    ```

    In this example, the `login_view` function is wrapped with the `unauthenticated_user` decorator. If a user who is already authenticated tries to access the login page, they will be redirected to the 'home' page.

    Note:
    - Make sure to use this decorator before any authentication-related views in your Django project.
    """
    def wrapper_func(request, *args, **kwargs):
        
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
        
    return wrapper_func