from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-login')
    else:
        form = CreateUserForm()    

    context = {
        'form': form
    }

    return render(request, 'user/register.html', context)

def login(request):
    return render(request, 'user/login.html')

def logout(request):
    return render(request, 'user/logout.html')

def profile(request):
    return render(request, 'user/profile.html')

def profile_update(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance = request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            return redirect('user-profile')

    else:
        user_update_form = UserUpdateForm(instance = request.user)
        profile_update_form = ProfileUpdateForm(instance = request.user.profile)
    
    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }

    return render(request, 'user/profile-update.html', context)
