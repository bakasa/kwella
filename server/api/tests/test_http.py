import base64
import json

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from sendsms import api
from users.models import Driver, Owner, Rider

PASSWORD = 'ilovethispassword'

def create_user(phone_number='0000000000', password=PASSWORD, usertype='RIDER', fname='Will', lname='Smith'):
    '''
    Helper function to ensure the code is DRY
    '''
    return get_user_model().objects.create_user(
        phone_number=phone_number,
        password=password,
        type=usertype,
        first_name=fname,
        last_name=lname,
        is_active=True
    )

class AuthenticationTest(APITestCase):

    client = APIClient()

    def setUp(cls):
        create_user()
        return super().setUp()

    def test_owner_can_signup(self):
        response = self.client.post(reverse('api:signup'), data={
            'phone_number': '1111111111',
            'first_name': 'Kendrick',
            'last_name': 'Lamar',
            'type': 'OWNER',
            'password': PASSWORD,
            'confirm_password': PASSWORD
        })

        user = get_user_model().objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)
        self.assertEqual(response.data['type'], 'OWNER')

    def test_driver_can_signup(self):
        response = self.client.post(reverse('api:signup'), data={
            'phone_number': '2222222222',
            'first_name': 'Kendrick',
            'last_name': 'Lamar',
            'type': 'DRIVER',
            'password': PASSWORD,
            'confirm_password': PASSWORD
        })

        user = get_user_model().objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)
        self.assertEqual(response.data['type'], 'DRIVER')

    def test_rider_can_signup(self):
        response = self.client.post(reverse('api:signup'), data={
            'phone_number': '3333333333',
            'first_name': 'Kendrick',
            'last_name': 'Lamar',
            'type': 'RIDER',
            'password': PASSWORD,
            'confirm_password': PASSWORD
        })

        user = get_user_model().objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)
        self.assertEqual(response.data['type'], 'RIDER')

    def test_user_can_login(self):
        user = get_user_model().objects.last()

        # login with created user credentials 
        response = self.client.post(reverse('api:login'), data={
            'phone_number': '0000000000',
            'password': PASSWORD
        }, format='json')



        # parse payload data from access token
        access = response.data['access']
        header, payload, signiture = access.split('.')
        decoded_payload = base64.b64decode(f'{payload}==')
        payload_data = json.loads(decoded_payload)

        # import pdb
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['refresh'])
        self.assertEqual(payload_data['user_id'], user.id)
        self.assertEqual(payload_data['phone_number'], user.phone_number)
        self.assertEqual(payload_data['first_name'], user.first_name)
        self.assertEqual(payload_data['last_name'], user.last_name)
        self.assertEqual(payload_data['type'], user.type)
