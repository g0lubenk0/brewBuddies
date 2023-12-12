from django.shortcuts import render, redirect
from .forms import CreateUserForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

"""
Profile Views Module

This module contains Django views related to user profiles, including profile editing, login, registration, and logout.

Functions:
    - index(request): Redirects the user to the 'map' page.
    
    - profile(request): Handles profile editing. If the request method is POST, updates the user's profile with the submitted form data. Redirects to the home page on successful update.
    
    - login_user(request): Handles user login. If the request method is POST, attempts to authenticate the user and logs them in. Displays an error message on invalid credentials.
    
    - register_user(request): Handles user registration. If the request method is POST, creates a new user using the submitted form data. Redirects to the login page on successful registration.
    
    - logout_user(request): Logs out the currently authenticated user and redirects to the login page.

Decorators:
    - unauthenticated_user: Custom decorator to restrict access to certain views for already authenticated users.

Dependencies:
    - Django: The views use various modules from Django, including shortcuts, forms, messages, authentication, and decorators.

Usage:
    Include these views in your Django app, and make sure to set up corresponding templates and URL configurations.
"""

def index(request):
    """
    Redirects the user to the 'map' page.
    """
    return redirect('map')

@login_required(login_url='login')
def profile(request):
    return render(request, 'profiles/profile.html')


@login_required(login_url='login')
def profile_edit(request):
    """
    Handles profile editing. If the request method is POST, updates the user's profile with the submitted form data.
    Redirects to the home page on successful update.
    """
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            username = request.user.username
            messages.success(request, f'{username}, Your profile is updated.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    context = {'form':form}
    return render(request, 'profiles/edit_profile.html', context)

@unauthenticated_user
def login_user(request):
    """
    Handles user login. If the request method is POST, attempts to authenticate the user and logs them in.
    Displays an error message on invalid credentials.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f'{username}, You are logged in.')
            return redirect('/')
        else:
            messages.info(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'profiles/login_page.html')

@unauthenticated_user
def register_user(request):
    """
    Handles user registration. If the request method is POST, creates a new user using the submitted form data.
    Redirects to the login page on successful registration.
    """
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            context = {'form':form}
            return render(request, 'profiles/register_page.html', context)
    
    context = {'form':form}
    return render(request, 'profiles/register_page.html', context)

@login_required(login_url='login')
def logout_user(request):
    """
    Logs out the currently authenticated user and redirects to the login page.
    """
    logout(request)
    messages.info(request, 'You logged put successfully')
    return redirect('login')

