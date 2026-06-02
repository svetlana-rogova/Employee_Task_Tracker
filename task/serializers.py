from rest_framework import serializers
from task.models import Employee, Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Сериализатор для задачи
    """
    class Meta:
        model = Task
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для сотрудника
    """
    task = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'middle_name', 'post', 'task']