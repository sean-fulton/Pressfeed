from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
import requests


def register(request):

    return render(request, 'accounts/register.html', {})


def login_view(request):

    return render(request, 'accounts/login.html', {})


def logout_view(request):
    return redirect('home')
