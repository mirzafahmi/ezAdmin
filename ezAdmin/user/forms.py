from django import forms
from django.contrib.auth.models import  User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class CreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email',]

class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['new_password1'].required = False
        self.fields['new_password2'].required = False

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone', 'image']