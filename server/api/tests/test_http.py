from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from users.models import Driver, Owner, Rider

PASSWORD = 'ilovethispassword'

class AuthenticationTest(APITestCase):
    def test_user_can_signup(self):
        response = self.client.post(reverse('signup'), data={
            'phone_number': '0712345689',
            'first_name': 'Kendrick',
            'last_name': 'Lamar',
            'password': PASSWORD,
            'confirm_password': PASSWORD
        })

        user = get_user_model().objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)
        self.assertEqual(response.data['type'], user.type)
        
