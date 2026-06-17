from rest_framework import viewsets
from rest_framework.decorators import action
from django.views.generic import TemplateView, UpdateView, CreateView
from django.shortcuts import redirect
from task.forms import TaskForm
from task.models import Task, Employee
from task.pagination import MyPagination
from task.permissions import IsOwner, IsModerator
from task.serializers import TaskSerializer, EmployeeSerializer
from django.db.models import Count, Q, Min
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


class TaskViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с задачами.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    pagination_class = MyPagination

    def perform_create(self, serializer):
        """
        Присваиваем пользователя владельцем при создании задачи
        """
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """
        Менять и удалять задачи может только владелец или модератор
        """
        if self.action in ['update', 'destroy']:
            self.permission_classes = [IsOwner | IsModerator]
        return [permission() for permission in self.permission_classes]

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


class TaskPageView(TemplateView):
    """
    Представление главной страницы со списком задач.
    """
    template_name = "task/home.html"


class AddTaskPageView(CreateView):
    """
    Представление для страницы добавления задачи.
    """
    model = Task
    form_class = TaskForm
    success_url = '/'
    template_name = "task/add_task.html"

    def form_valid(self, form):
        """
        Сохраняет задачу и назначает её владельцем текущего пользователя.
        """
        self.object = form.save(user=self.request.user)
        return redirect(self.success_url)


class ImportantTaskPageView(TemplateView):
    """
    Представление для страницы с отображением важных задач.
    """
    template_name = "task/important.html"


class EmployeePageView(TemplateView):
    """
    Представление для страницы с отображением сотрудников.
    """
    template_name = "task/employee.html"


class TaskEditView(UpdateView):
    """
    Представление для страницы изменения задачи.
    """
    model = Task
    fields = ['title', 'status', 'period', 'parent_task', 'executor']
    template_name = 'task/edit.html'
    success_url = '/'
    serializer_class = TaskSerializer

    def get_queryset(self):
        """
        Менять могут только владельцы или модератор
        """
        if self.request.user.groups.filter(name='moderator').exists():
            return Task.objects.all()
        return Task.objects.filter(owner=self.request.user)
