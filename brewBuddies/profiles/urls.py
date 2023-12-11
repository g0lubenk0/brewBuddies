from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)


urlpatterns = [
    path('', views.index, name='home'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/login/', views.login_user, name='login'),
    path('accounts/register/', views.register_user, name='register'),
    path('accounts/logout/', views.logout_user, name='logout'),
    path('accounts/password_reset/', PasswordResetView.as_view(template_name="profiles/password_reset.html"), name='password_reset'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(template_name="profiles/password_reset_done.html"), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="profiles/password_reset_confirm.html"), name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(template_name="profiles/password_reset_complete.html"), name='password_reset_complete'),
]
