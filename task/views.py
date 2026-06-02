from rest_framework import viewsets

from task.models import Task, Employee
from task.serializers import TaskSerializer, EmployeeSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с задачами.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с сотрудниками.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer