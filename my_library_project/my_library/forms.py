from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Поле для електронної пошти, обов'язкове для заповнення

    class Meta:
        model = User  # Модель User використовується для створення нового користувача
        fields = ['username', 'email', 'password1', 'password2']  # Поля, що відображатимуться у формі

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username")  # Поле для імені користувача з підписом "Username"
    password = forms.CharField(widget=forms.PasswordInput)  # Поле для пароля з маскуванням введення

