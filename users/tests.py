from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class UserPokeTests(APITestCase):

    def setUp(self):
        data = {"user": {"email": "test@test.com", "password": "test", "password2": "test"}}
        self._create_user(data)

    def _create_user(self, data):
        url = reverse('user:registration')
        response = self.client.post(url, data)
        return response

    def _login_user(self, data):
        url = reverse('user:login')
        response = self.client.post(url, data)
        return response

    def test_create_user(self):
        """
            Test create user
        """
        data = {"user": {"email": "root@root.com", "password": "root", "password2": "root"}}
        response = self._create_user(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'root@root.com')

    def test_login_user(self):
        """
            Test login user
        """
        data = {"user": {"email": "test@test.com", "password": "test"}}
        response = self._login_user(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@test.com')