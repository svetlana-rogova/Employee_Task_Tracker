from rest_framework import serializers
from task.models import Employee, Task
from task.validators import validate_period, validate_not_self_parent, validate_executor_for_in_progress


class TaskSerializer(serializers.ModelSerializer):
    """
    Сериализатор для задачи
    """
    can_edit = serializers.SerializerMethodField()
    can_delete = serializers.SerializerMethodField()

    executor = serializers.SlugRelatedField(
        many=True,
        queryset=Employee.objects.all(),
        slug_field='last_name'
    )

    parent_task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(),
        required=False,
        allow_null=True
    )

    parent_task_title = serializers.SlugRelatedField(
        source='parent_task',
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
        fields = ['id', 'title', 'executor', 'period', 'status', 'children_task', 'parent_task', 'parent_task_title',
                  'can_edit', 'can_delete']

    def validate(self, attrs):
        period = attrs.get("period", self.instance.period if self.instance else None)
        parent_task = attrs.get('parent_task')
        status = attrs.get('status')
        executor = attrs.get('executor')
        instance = self.instance
        validate_period(period)
        validate_not_self_parent(instance, parent_task)
        validate_executor_for_in_progress(status, executor)
        return attrs

    def is_moderator(self, user):
        """
        Проверяет, состоит ли пользователь в группе moderator.
        """
        return user.groups.filter(name='moderator').exists()

    def get_can_edit(self, obj):
        """
            Возвращает True, если текущий пользователь может редактировать задачу (является ее владельцем или
            модератором)
        """
        user = self.context['request'].user

        if not user.is_authenticated:
            return False
        return obj.owner == user or self.is_moderator(user)

    def get_can_delete(self, obj):
        """
            Возвращает True, если текущий пользователь может удалить задачу (является ее владельцем или модератором)
        """
        user = self.context['request'].user

        if not user.is_authenticated:
            return False
        return obj.owner == user or self.is_moderator(user)


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для сотрудника
    """
    active_tasks = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'middle_name', 'post', 'active_tasks']

    def get_active_tasks(self, obj):
        """
        Возвращает активные задачи сотрудника
        """
        active_tasks = obj.task.filter(status='in_progress')
        return [task.title for task in active_tasks]
