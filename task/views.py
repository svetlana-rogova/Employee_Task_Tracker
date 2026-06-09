from rest_framework import viewsets
from rest_framework.decorators import action

from task.models import Task, Employee
from task.serializers import TaskSerializer, EmployeeSerializer
from django.db.models import Count, Q, Min
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
         Эндпоинт важных задач с указанием срока и списка подходящих сотрудников (ФИО) (Важные задачи: не взяты в
         работу, но от которых зависят другие задачи, взятые в работу.) (Подходящие сотрудники:
         (наименее загруженный сотрудник или сотрудник, выполняющий родительскую задачу, если ему назначено максимум
         на 2 задачи больше, чем у наименее загруженного сотрудника).
        """
        important_task = Task.objects.filter(status='created', children_tasks__status='in_progress').distinct()

        employees = Employee.objects.annotate(task_count=Count('task',
                                                               filter=Q(task__status__in=['created', 'in_progress'])))

        min_load = employees.aggregate(Min('task_count'))['task_count__min']

        max_allowed_load = min_load + 2

        result = []

        for task in important_task:

            least_loaded = employees.filter(task_count=min_load)

            parent_employees = Employee.objects.none()

            if task.parent_task:
                parent_employees = employees.filter(
                    id__in=task.parent_task.executor.values_list('id', flat=True), task_count__lte=max_allowed_load)

            candidates = (least_loaded | parent_employees).distinct()

            employee_names = [
                f"{employee.last_name} "
                f"{employee.first_name} "
                f"{employee.middle_name}"
                for employee in candidates
            ]

            result.append({
                'important_task': task.title,
                'period': task.period.strftime("%d.%m.%Y %H:%M"),
                'employees': employee_names
            })

        return Response(result)


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
