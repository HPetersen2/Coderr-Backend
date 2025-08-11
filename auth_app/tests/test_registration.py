from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class RegistrationTest(APITestCase):

    def test_post_user(self):
        url = 'http://127.0.0.1:8000/api/registration/'
        data = {
            'username': 'Hans Peter',
            'email': 'hanspeter@coderr.de',
            'password': 'secure123',
            'repeated_password': 'secure123',
            'type': 'business',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)