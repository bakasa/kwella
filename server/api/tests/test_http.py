import base64
import json
import pdb
from io import BytesIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from trips.models import Trip
from trips.serializers import TripSerializer
from users.models import Driver, Owner, Rider
from users.serializers import UserSerializer
from users.textchoices import UserTypes

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

def create_photo_file():
    data = BytesIO()
    Image.new('RGB', (100, 100)).save(data, 'PNG')
    data.seek(0)

    return SimpleUploadedFile('photo.png', data.getvalue())
class AuthenticationTest(APITestCase):

    def setUp(self):
        create_user()
        self.photo_file = create_photo_file()
        
        # users groups
        Group.objects.create(name='owners')
        Group.objects.create(name='riders')
        Group.objects.create(name='drivers')

        return super().setUp()

    def test_owner_can_signup(self):
        response = self.client.post(reverse('api:signup'), data={
            'phone_number': '1111111111',
            'first_name': 'Kendrick',
            'last_name': 'Lamar',
            'type': 'OWNER',
            'password': PASSWORD,
            'confirm_password': PASSWORD,
            'photo': self.photo_file
        })

        user = get_user_model().objects.last()
        # import pdb; pdb.set_trace()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)
        self.assertEqual(response.data['type'], 'OWNER')
        self.assertIsNotNone(user.photo)
        # self.assertEqual(response.data['group'], 'owners')

    def test_driver_can_signup(self):
        response = self.client.post(reverse('api:signup'), data={
            'phone_number': '2222222222',
            'first_name': 'Kendrick',
            'last_name': 'Lamar',
            'type': 'DRIVER',
            'password': PASSWORD,
            'confirm_password': PASSWORD,
            'photo': self.photo_file
        })

        user = get_user_model().objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)
        self.assertEqual(response.data['type'], 'DRIVER')
        self.assertIsNotNone(user.photo)
        # self.assertEqual(response.data['group'], 'drivers')

    def test_rider_can_signup(self):
        response = self.client.post(reverse('api:signup'), data={
            'phone_number': '3333333333',
            'first_name': 'Kendrick',
            'last_name': 'Lamar',
            'type': 'RIDER',
            'password': PASSWORD,
            'confirm_password': PASSWORD,
            'photo': self.photo_file
        })

        user = get_user_model().objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], user.id)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)
        self.assertEqual(response.data['type'], 'RIDER')
        self.assertIsNotNone(user.photo)
        # self.assertEqual(response.data['group'], 'riders')

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

class HttpTripsTest(APITestCase):
    client = APIClient()

    def setUp(self):
        # create driver
        self.driver = create_user(usertype=UserTypes.driver.value, phone_number='0781234569')

        # create rider
        self.rider = create_user()
        rider_response = self.client.post(reverse('api:login'), data={'phone_number': self.rider.phone_number, 'password': PASSWORD})

        self.access = rider_response.data['access']

        # force authenticate rider
        self.client.force_authenticate(user=self.rider, token=self.access)

        # create trips
        Trip.objects.create(pickup='A', dropoff='B', rider=self.rider, driver=self.driver)
        Trip.objects.create(pickup='E', dropoff='F', driver=self.driver)
        Trip.objects.create(pickup='C', dropoff='D', rider=self.rider)
        return super().setUp()
    
    def test_user_list_trips(self):
        
        trips = Trip.objects.filter(rider=self.rider)

        response = self.client.get(reverse('api:trips-list'))

        expected_trip_ids = [str(trip.id) for trip in trips]
        actual_trip_ids = [trip.get('id') for trip in response.data]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertCountEqual(expected_trip_ids, actual_trip_ids)
        self.assertEqual(len(response.data), trips.count())

    def test_user_can_retrieve_single_trip(self):
        trip = Trip.objects.filter(rider=self.rider).first()

        response = self.client.get(trip.get_absolute_url())

        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), str(trip.id))


