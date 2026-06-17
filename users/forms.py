from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Класс, который задает форму для регистрации
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']


class UserProfile(forms.ModelForm):
    """
    Класс, который задает форму для профиля пользователя
    """
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'middle_name', 'post', 'phone_number', 'email']
