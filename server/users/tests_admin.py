from django.contrib.auth import get_user_model
from django.test import TestCase
from users.models import Driver, Owner, Rider


class UserManagerTestCase(TestCase):
    def test_create_user(self):
        User = get_user_model()

        user = User.objects.create(
            phone_number='0724446666', password='ilovethispassword')
        self.assertEqual(user.phone_number, '0724446666')
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff) 
        self.assertFalse(user.is_superuser)

        with self.assertRaises(ValueError):
            # phone number must be 10 digits min
            User.objects.create_user(
                phone_number='071234567', password='ilovethispassword')

        with self.assertRaises(ValueError):
            # phone number must be 10 digits max
            User.objects.create_user(
                phone_number='07123456789', password='ilovethispassword')


        with self.assertRaises(TypeError):
            # can't create user with no credentials
            User.objects.create_user()

        with self.assertRaises(TypeError):
            # must provide phone number
            User.objects.create_user(phone_number='')

        with self.assertRaises(ValueError):
            # must provide phone number
            User.objects.create_user(
                phone_number='', password='ilovethispassword')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(phone_number='0712345689', password='ilovethispassword')

        self.assertEqual(admin_user.phone_number, '0712345689')
        self.assertEqual(admin_user.type, 'OWNER')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        

        with self.assertRaises(ValueError):
            # superuser attribute must be true
            User.objects.create_superuser(phone_number='0756667777', password='ilovethispassword', is_superuser=False)

class OwnerManagerTestCase(TestCase):

    def test_create_owner(self):
        users = get_user_model().objects.all()
        owner = Owner.owners.create(phone_number='0712345689', password='ilovethispassword')

        self.assertEqual(owner.phone_number, '0712345689')
        self.assertEqual(owner.type, 'OWNER')
        self.assertEqual(users.count(), 1)
        self.assertFalse(owner.is_active)
        self.assertFalse(owner.is_superuser)
        self.assertTrue(owner.is_staff)

class RiderManagerTestCase(TestCase):

    def test_create_rider(self):
        users = get_user_model().objects.all()
        rider = Rider.riders.create(phone_number='0712345689', password='ilovethispassword')

        self.assertEqual(rider.phone_number, '0712345689')
        self.assertEqual(rider.type, 'RIDER')
        self.assertEqual(users.count(), 1)
        self.assertFalse(rider.is_active)
        self.assertFalse(rider.is_superuser)
        self.assertFalse(rider.is_staff)





