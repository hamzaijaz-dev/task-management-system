from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch


class HomeViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test_user', password='test_password')

    def test_home_view_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('login') + '?next=/')

    def test_home_view_loads_when_logged_in(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_app.html')

    @patch('todo.views.requests.post')
    def test_create_todo_failure(self, mock_post):
        mock_post.return_value.status_code = 400
        self.client.login(username='test_user', password='test_password')
        response = self.client.post(reverse('home'), {
            'title': 'Test Todo',
            'description': 'Test Description',
            'due_date': '2024-03-20',
            'status': 'PENDING'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_app.html')

    @patch('todo.views.requests.get')
    def test_home_view_with_todos(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'my_todos': [
                {'id': 1, 'title': 'Test Todo 1', 'description': 'Test Description 1',
                 'due_date': '2024-03-20', 'status': 'PENDING'
                 }
            ],
            'assigned_todos': [
                {'id': 2, 'title': 'Test Todo 2', 'description': 'Test Description 2',
                 'due_date': '2024-03-21', 'status': 'IN_PROGRESS'
                 }
            ]
        }
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_app.html')
        self.assertContains(response, 'Test Todo 1')
        self.assertContains(response, 'Test Todo 2')

    @patch('todo.views.requests.get')
    def test_home_view_without_todos(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'my_todos': [],
            'assigned_todos': []
        }
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_app.html')
        self.assertNotContains(response, 'Test Todo 1')
        self.assertNotContains(response, 'Test Todo 2')
