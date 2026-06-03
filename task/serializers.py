from rest_framework import serializers
from task.models import Employee, Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Сериализатор для задачи
    """
    executor = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='last_name'
    )

    parent_task = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )

    children_task = serializers.SlugRelatedField(
        source='children_tasks',
        many=True,
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = Task
        fields = ['title', 'executor', 'period', 'status', 'children_task', 'parent_task']






class EmployeeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для сотрудника
    """
    active_tasks = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'middle_name', 'post', 'active_tasks']

    def get_active_tasks(self, obj):
        active_tasks = obj.task.filter(status='in_progress')
        return [task.title for task in active_tasks]