from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagerTestCase(TestCase):
    def test_create_user(self):
        User = get_user_model()

        user = User.objects.create(
            phone_number='0724446666', password='ilovethispassword')
        self.assertEqual(user.phone_number, '0724446666')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff) 
        self.assertFalse(user.is_superuser)

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
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            # superuser attribute must be true
            User.objects.create_superuser(phone_number='0756667777', password='ilovethispassword', is_superuser=False)





