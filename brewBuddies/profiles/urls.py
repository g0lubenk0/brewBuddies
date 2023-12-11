from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('password_reset/', PasswordResetView.as_view(template_name="profiles/password_reset.html"), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name="profiles/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name="profiles/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name="profiles/password_reset_complete.html"), name='password_reset_complete'),
]
