from django.test import TestCase, Client
from django.urls import reverse
from .models import Todo


class TodoModelTest(TestCase):
    def test_str(self):
        todo = Todo(title='Buy milk')
        self.assertEqual(str(todo), 'Buy milk')

    def test_default_completed_false(self):
        todo = Todo.objects.create(title='Test task')
        self.assertFalse(todo.completed)


class TodoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(title='First task')

    def test_home_returns_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'First task')

    def test_health_endpoint(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'ok', **{'uptime': response.json()['uptime']}})

    def test_create_todo(self):
        response = self.client.post(
            reverse('todo-create'),
            {'title': 'New task'},
        )
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Todo.objects.filter(title='New task').exists())

    def test_create_todo_empty_title_ignored(self):
        count_before = Todo.objects.count()
        self.client.post(reverse('todo-create'), {'title': '   '})
        self.assertEqual(Todo.objects.count(), count_before)

    def test_toggle_todo(self):
        response = self.client.post(reverse('todo-toggle', args=[self.todo.pk]))
        self.assertRedirects(response, reverse('home'))
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.completed)

    def test_delete_todo(self):
        pk = self.todo.pk
        response = self.client.post(reverse('todo-delete', args=[pk]))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Todo.objects.filter(pk=pk).exists())
