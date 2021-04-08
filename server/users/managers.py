from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    '''
    Custom user model manager where phone number is the unique identifier for authentication, instead of usernames
    '''

    def create_user(self, phone_number, password, **extra_fields):
        '''
        Create and save User with given phone number and password
        '''

        if not phone_number:
            raise ValueError(
                _('We\'ll need your phone number to get you going!'))

        if len(phone_number) < 10:
            raise ValueError(_('This phone number is too short!'))

        if len(phone_number) > 10:
            raise ValueError(_('This phone number is too long!'))

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        '''
        Create and save Superuser with given phone number and password
        '''

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('type', 'OWNER')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have staff privileges'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have superuser privileges'))

        return self.create_user(phone_number, password, **extra_fields)


class OwnerManager(models.Manager):
    '''
    Create user of type Taxi Owner
    '''

    def get_queryset(self):
        return super().get_queryset().filter(type=get_user_model().Types.OWNER)


class DriverManager(models.Manager):
    '''
    Create user of type Taxi Driver
    '''

    def get_queryset(self):
        return super().get_queryset().filter(type=get_user_model().Types.DRIVER)


class RiderManager(models.Manager):
    '''
    Create user of type Rider
    '''

    def get_queryset(self):
        return super().get_queryset().filter(type=get_user_model().Types.RIDER)
