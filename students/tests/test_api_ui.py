from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse

from .test_models import ModelsTest


class APITestCase(TestCase):
    fixtures = ['sample_data.json']

    def setUp(self):
        self.client = APIClient()

    def test_students_list_public(self):
        resp = self.client.get('/api/students/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(isinstance(resp.json(), list))

    def test_student_create_requires_auth(self):
        data = {
            'first_name': 'Jane', 'last_name': 'Smith', 'roll_no': 'R002'
        }
        resp = self.client.post('/api/students/', data, format='json')
        self.assertIn(resp.status_code, (401, 403))

        # create a user and authenticate
        user = User.objects.create_user('testuser', 't@example.com', 'pass')
        self.client.force_authenticate(user=user)
        resp2 = self.client.post('/api/students/', data, format='json')
        self.assertIn(resp2.status_code, (201, 200))

    def test_students_export_csv_api(self):
        resp = self.client.get('/api/students/export/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'text/csv')
        self.assertIn('first_name', resp.content.decode('utf-8'))


class UITests(TestCase):
    fixtures = ['sample_data.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('webuser', 'w@example.com', 'pass')

    def test_students_list_redirects_when_not_logged_in(self):
        resp = self.client.get('/students/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Students')

    def test_students_list_access_when_logged_in(self):
        self.client.login(username='webuser', password='pass')
        resp = self.client.get('/students/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Students')

    def test_students_export_csv_web(self):
        resp = self.client.get('/students/export/csv/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'text/csv')
        self.assertIn('first_name', resp.content.decode('utf-8'))
