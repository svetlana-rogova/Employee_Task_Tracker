from datetime import datetime
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from task.models import Task, Employee


class TaskTestCase(APITestCase):

    def setUp(self) -> None:
        """
        Создаем тестовые данные
        """

        self.client = APIClient()

        self.one_employee = Employee.objects.create(
            first_name="test",
            last_name="test",
            post="it специалист"
        )

        self.two_employee = Employee.objects.create(
            first_name="test2",
            last_name="Сотрудник без задач",
            post="it специалист"
        )

        self.three_employee = Employee.objects.create(
            first_name="test3",
            last_name="Сотрудник для главной задачи",
            post="it специалист"
        )

        self.parent_task1 = Task.objects.create(
            title="Презентация нашей компании в сети",
            period=datetime(2026, 6, 2, 10, 0),
            status="in_progress"
        )

        self.parent_task = Task.objects.create(
            title="Работа над сайтом нашей компании",
            period=datetime(2026, 6, 2, 10, 0),
            status="created"
        )

        self.child_task = Task.objects.create(
            title="Разработка главной страницы",
            period=datetime(2026, 6, 3, 11, 0),
            status="in_progress"
        )

        self.task_no_important = Task.objects.create(
            title="Обычная задача",
            period=datetime(2026, 6, 4, 12, 0),
            status="created"
        )

        self.parent_task1.executor.add(self.three_employee)
        self.child_task.executor.add(self.three_employee)
        self.child_task.executor.add(self.one_employee)
        self.parent_task.parent_task = self.parent_task1
        self.parent_task.save()
        self.child_task.parent_task = self.parent_task
        self.child_task.save()

    def test_create_task(self):
        """
        Проверка на создание задачи
        """
        data = {
            "title": "Новая задача",
            "period": "2026-06-02T10:00:00Z",
            "status": "created"
        }
        response = self.client.post(reverse("task:task-list"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 5)

    def test_update_task(self):
        """
        Проверка на обновление задачи
        """
        data = {
            "title": "Обычная задача 2",
            "period": "2026-06-02T10:00:00Z",
            "status": "created"
        }

        response = self.client.put(reverse("task:task-detail", args=[self.task_no_important.id]), data)
        self.assertEqual(response.status_code, 200)

    def test_get_task_list(self):
        """
        Проверка на получение списка задач
        """
        response = self.client.get(reverse("task:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)

    def test_task_delete(self):
        """
        Проверка на удаление задачи
        """
        response = self.client.delete(reverse("task:task-detail", args=[self.task_no_important.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Task.objects.count(), 3)

    def test_create_employee(self):
        """
        Проверка на создание сотрудника
        """
        data = {
            "first_name": "Новый",
            "last_name": "сотрудник",
            "post": "сотрудник"
        }
        response = self.client.post(reverse("task:employee-list"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Employee.objects.count(), 4)

    def test_update_employee(self):
        """
        Проверка на обновление сотрудника
        """
        data = {
            "first_name": "Новый",
            "last_name": "сотрудник",
            "post": "сотрудник"
        }

        response = self.client.put(reverse("task:employee-detail", args=[self.two_employee.id]), data)
        self.assertEqual(response.status_code, 200)

    def test_get_employee_list(self):
        """
        Проверка на получение списка сотрудников
        """
        response = self.client.get(reverse("task:employee-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)

    def test_employee_delete(self):
        """
        Проверка на удаление сотрудника
        """
        response = self.client.delete(reverse("task:employee-detail", args=[self.two_employee.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Employee.objects.count(), 2)

    def test_task_important(self):
        """
        Тест на вывод важных задач
        """
        response = self.client.get(reverse("task:task-important"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        print(response.data)
        self.assertEqual(response.data[0]['important_task'], 'Работа над сайтом нашей компании')
        self.assertCountEqual(response.data[0]['employees'],
                              ['Сотрудник без задач test2 ', 'Сотрудник для главной задачи test3 '])

    def test_task_busy(self):
        """
        Тест на вывод сотрудников по порядку загруженности
        """
        response = self.client.get(reverse("task:employee-busy"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        print(response.data)
        self.assertEqual(response.data[0]['first_name'], 'test3')
        self.assertEqual(response.data[1]['first_name'], 'test')
        self.assertEqual(response.data[2]['first_name'], 'test2')

    def test_task_important_empty(self):
        """
        Нет важных задач
        """
        Task.objects.all().delete()
        response = self.client.get(reverse("task:task-important"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_task_important_not(self):
        """
        Есть задачи, но они не подходят под критерий important
        """
        Task.objects.all().update(status='done')
        response = self.client.get(reverse("task:task-important"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_employee_not_found(self):
        """
        Проверка получения несуществующего сотрудника
        """
        response = self.client.get(reverse("task:employee-detail", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_task_important_not_found(self):
        """
        Проверка получения несуществующей задачи
        """
        response = self.client.get(reverse("task:task-detail", args=[999]))
        self.assertEqual(response.status_code, 404)
