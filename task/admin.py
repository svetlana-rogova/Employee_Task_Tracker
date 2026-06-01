from django.contrib import admin

from task.models import Employee, Task


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'middle_name', 'post')
    search_fields = ('last_name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent_task', 'period', 'status')
    search_fields = ('period',)