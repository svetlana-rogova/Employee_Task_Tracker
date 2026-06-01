from django.db import models


class Employee(models.Model):
    """
    Модель сотрудника
    """
    first_name = models.CharField(max_length=150, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    middle_name = models.CharField(max_length=150, blank=True, verbose_name='отчество')
    post = models.CharField(max_length=150, verbose_name='должность')

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name} {self.post}'

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'
        ordering = ['last_name']


class Task(models.Model):
    """
    Модель задачи
    """
    Created = 'created'
    In_Progress = 'in_progress'
    Done = 'done'

    STATUS_CHOICES = [
        ('created', 'создана'),
        ('in_progress', 'выполняется'),
        ('done', 'закончена'),
    ]

    title = models.CharField(max_length=150, verbose_name='наименование')
    parent_task = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="children_tasks", verbose_name='ссылка на родительскую задачу')
    executor = models.ManyToManyField('Employee', verbose_name='исполнитель', blank=True, related_name="task")
    period = models.DateTimeField(verbose_name='срок')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='created', verbose_name='статус')

    def __str__(self):
        return f'Задача: "{self.title}", статус: {self.status}'

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'
        ordering = ['period']
