from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm
from .models import CustomUser
from .forms import UserProfile


class RegisterView(CreateView):
    """
    Класс для регистрации пользователя
    """
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('task:home')


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Класс для профиля пользователя с возможностью изменения
    """
    model = CustomUser
    form_class = UserProfile
    template_name = 'users/profile.html'
    success_url = reverse_lazy('task:home')

    def get_object(self):
        return self.request.user
