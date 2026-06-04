from rest_framework.routers import DefaultRouter
from task.views import TaskViewSet, EmployeeViewSet

app_name = 'task'

router = DefaultRouter()
router.register(r'task', TaskViewSet, basename='task')
router.register(r'employee', EmployeeViewSet, basename='employee')

urlpatterns = router.urls
