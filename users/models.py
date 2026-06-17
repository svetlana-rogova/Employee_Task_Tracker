from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Модель пользователя
    """
    first_name = models.CharField(max_length=150, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    middle_name = models.CharField(max_length=150, blank=True, verbose_name='отчество')
    post = models.CharField(max_length=150, verbose_name='должность')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.last_name} {self.post} {self.email}'
