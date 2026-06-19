from rest_framework.routers import DefaultRouter
from task.views import (TaskViewSet, EmployeeViewSet, TaskPageView, AddTaskPageView, ImportantTaskPageView,
                        EmployeePageView, TaskEditView)
from django.urls import path, include

app_name = 'task'

router = DefaultRouter()
router.register(r'task', TaskViewSet, basename='task')
router.register(r'employee', EmployeeViewSet, basename='employee')


urlpatterns = [
    path("", TaskPageView.as_view(), name="home"),
    path("employee/", EmployeePageView.as_view(), name="employee"),
    path("task_add/", AddTaskPageView.as_view(), name='add_task'),
    path("important/", ImportantTaskPageView.as_view(), name='important'),
    path("api/", include(router.urls)),
    path('task/<int:pk>/edit/', TaskEditView.as_view(), name='edit'),
]
