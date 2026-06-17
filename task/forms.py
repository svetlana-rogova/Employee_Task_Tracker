from django import forms

from task.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'status', 'period', 'parent_task', 'executor']

    def clean(self):
        cleaned_data = super().clean()

        status = cleaned_data.get('status')
        executors = cleaned_data.get('executor')

        if status == 'in_progress' and (not executors or len(executors) == 0):
            self.add_error('executor', 'Для задачи со статусом in_progress необходимо назначить исполнителя.')

        return cleaned_data

    def save(self, commit=True, user=None):
        obj = super().save(commit=False)

        if user:
            obj.owner = user

        if commit:
            obj.save()
            self.save_m2m()

        return obj