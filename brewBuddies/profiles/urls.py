from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

"""
URL Patterns for User Authentication and Profile Management

This module defines the URL patterns for various user authentication and profile management views in a Django web application.

URL Patterns:
- `/`: Home page view (index).
- `/accounts/profile/`: User profile view (profile).
- `/accounts/login/`: User login view (login_user).
- `/accounts/register/`: User registration view (register_user).
- `/accounts/logout/`: User logout view (logout_user).
- `/accounts/password_reset/`: Password reset view (PasswordResetView) with associated template (password_reset.html).
- `/accounts/password_reset/done/`: Password reset done view (PasswordResetDoneView) with associated template (password_reset_done.html).
- `/accounts/reset/<uidb64>/<token>/`: Password reset confirm view (PasswordResetConfirmView) with associated template (password_reset_confirm.html).
- `/accounts/reset/done/`: Password reset complete view (PasswordResetCompleteView) with associated template (password_reset_complete.html).

View Functions:
- `index`: Home page view.
- `profile`: User profile view.
- `login_user`: User login view.
- `register_user`: User registration view.
- `logout_user`: User logout view.

Note: The views for password reset are provided by Django's built-in PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, and PasswordResetCompleteView.

Usage:
Include these URL patterns in your Django project's main `urls.py` using the `include` function:
    ```
    from django.urls import path, include

    urlpatterns = [
        # ... other patterns ...
        path('', include('your_app_name.urls')),
    ]
    ```

"""

urlpatterns = [
    path('', views.index, name='home'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/edit', views.profile_edit, name='profile_edit'),
    path('accounts/login/', views.login_user, name='login'),
    path('accounts/register/', views.register_user, name='register'),
    path('accounts/logout/', views.logout_user, name='logout'),
    path('accounts/search_profile/', views.search_profiles, name='search'),
    path('accounts/password_reset/', PasswordResetView.as_view(template_name="profiles/password_reset.html"), name='password_reset'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(template_name="profiles/password_reset_done.html"), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="profiles/password_reset_confirm.html"), name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(template_name="profiles/password_reset_complete.html"), name='password_reset_complete'),
]
