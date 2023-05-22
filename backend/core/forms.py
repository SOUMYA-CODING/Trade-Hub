from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from . models import *


# Login
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


# Password Rest
class PasswordResetForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


# Registration
class RegistrationForm(UserCreationForm):
    username = forms.CharField(label="Username", max_length=100)
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# Parent Category
class ParentCategoryForm(forms.ModelForm):
    class Meta:
        models = ParentCategory
        fields = '__all__'