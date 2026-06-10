from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_period(period):
    """
    Дата выполнения не может быть в прошлом
    """
    if period < timezone.now():
        raise ValidationError('Срок выполнения не может быть в прошлом.')


def validate_not_self_parent(instance, parent_task):
    """
    Родительская задача не может быть родителем сама себе
    """
    if instance and parent_task == instance:
        raise ValidationError('Задача не может быть родительской для самой себя.')


def validate_executor_for_in_progress(status, executor):
    """
    Если задача в процессе выполнения, то у нее должен быть исполнитель
    """
    if status == 'in_progress' and not executor:
        raise ValidationError('Для задачи со статусом in_progress необходимо назначить исполнителя.')