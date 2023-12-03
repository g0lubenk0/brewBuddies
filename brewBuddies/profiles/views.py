from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Home page.")

def profile(request):
    return HttpResponse("Profile page.")

def login(request):
    return HttpResponse("Login page.")

def register(request):
    return HttpResponse("Register page.")

def logout(request):
    return HttpResponse("Logout page.")