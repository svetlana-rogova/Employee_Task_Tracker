from rest_framework import serializers
from task.models import Employee, Task


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для сотрудника
    """
    class Meta:
        model = Employee
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    """
    Сериализатор для задачи
    """
    class Meta:
        model = Task
        fields = '__all__'
