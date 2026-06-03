from rest_framework import viewsets
from rest_framework.decorators import action

from task.models import Task, Employee
from task.serializers import TaskSerializer, EmployeeSerializer
from django.db.models import Count, Q
from rest_framework.response import Response


class TaskViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с задачами.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False, methods=['get'])
    def important(self, request):
        """
        Эндпоинт важных задач (те задачи, которые не взяты в работу, но от которых зависят другие задачи,
        взятые в работу.)
        """
        important_task = Task.objects.filter(status='created', children_tasks__status='in_progress').distinct()
        serializer = TaskSerializer(important_task, many=True)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с сотрудниками.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=False, methods=['get'])
    def busy(self, request):
        """
        Эндпоинт для вывода сотрудников с активными задачами и сортировкой по ним
        """
        employee_tasks = Employee.objects.annotate(
            task_count_progress=Count('task', filter=Q(task__status='in_progress'))).order_by('-task_count_progress')
        serializer = EmployeeSerializer(employee_tasks, many=True)
        return Response(serializer.data)