from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from pressfeed.forms import RegisterUserForm, UsernameEditForm, ChangePasswordForm
from django.contrib import messages


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('Registered Successfully'))
            return redirect('home')
    else:
        form = RegisterUserForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in"))
            return redirect('login')
    else:
        return render(request, 'accounts/login.html', {})


@login_required
def account(request):
    if request.method == 'POST':
        username = request.user.username
        confirm_password = request.POST.get('conf-password')
        user = authenticate(request, username=username,
                            password=confirm_password)

        if user is not None:
            form = UsernameEditForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, ("Updated username!"))
                return redirect('account')
        else:
            messages.error(request, ("You password was not correct!"))
            form = UsernameEditForm(instance=request.user)

    else:
        form = UsernameEditForm(instance=request.user)
    return render(request, 'accounts/account.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Password updated!"))
            return redirect('login')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'accounts/password.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, ("You logged out successfully"))
    return redirect('home')


@login_required
@require_POST
def delete_account(request):
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, 'Your account has been deleted!')
    return redirect('home')