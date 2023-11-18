from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm, PasswordChangeForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, message = f'Account has been created for {username}. Please log in')
            return redirect('user-login')
    else:
        form = CreateUserForm()    

    context = {
        'form': form
    }

    return render(request, 'user/register.html', context)

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('dashboard-index')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form': form})

def logout(request):
    return render(request, 'user/logout.html')

@login_required
def profile(request):
    return render(request, 'user/profile.html')

@login_required
def profile_update(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        password_change_form = PasswordChangeForm(request.user, request.POST)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()

            # Check if the password change form is valid and if the user wants to change the password
            if password_change_form.is_valid() and password_change_form.cleaned_data['new_password1']:
                password_change_form.save()
                messages.success(request, 'Your password was successfully updated.')
            
            messages.success(request, 'Your profile was successfully updated.')
            
            return redirect('user-profile')

    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)
        password_change_form = PasswordChangeForm(request.user)

    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form,
        'password_change_form': password_change_form,
    }

    return render(request, 'user/profile-update.html', context)
