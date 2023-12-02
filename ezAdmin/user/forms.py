from django import forms
from django.contrib.auth.models import  User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from phonenumber_field.modelfields import PhoneNumberField
from mixins.file_size_mixin import FileValidatorMixin


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        user_exists = User.objects.filter(username=username).exists()

        if not user_exists:
            self.add_error('username', 'This username does not exist.')

        if username and password and not authenticate(username=username, password=password):
            self.add_error('password', 'Invalid password.')

        return cleaned_data


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

class IntlTelInputField(forms.CharField):
    widget = forms.TextInput(attrs={'class': 'intl-tel-input', 'type': 'tel', 'maxlength': '15'})

    def to_python(self, value):
        # Override this method to customize how the phone number is processed
        # For example, you might want to strip spaces or format it differently
        return super().to_python(value)

class ProfileUpdateForm(FileValidatorMixin, forms.ModelForm):
    phone = IntlTelInputField()

    allowed_extensions = ['png', 'jpeg']
    class Meta:
        model = Profile
        fields = ['address', 'phone', 'image']

    def clean_phone(self):
        phone_number = self.cleaned_data["phone"]

        cleaned_phone_number = ''.join(filter(str.isdigit, str(phone_number)))
        
        formatted_phone_number = f"+{cleaned_phone_number[0:2]} {cleaned_phone_number[2:4]}-{cleaned_phone_number[4:7]} {cleaned_phone_number[7:]}"

        return formatted_phone_number

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')

        self.validate_file_size(image, 'image')
        self.validate_file_extension(image, 'image')

        return cleaned_data
