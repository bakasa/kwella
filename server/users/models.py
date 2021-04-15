import random
from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, Group,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_otp.oath import TOTP

from .managers import (CustomUserManager, DriverManager, OwnerManager, RiderManager)
from .textchoices import UserTypes


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(_("First Name"), max_length=50, null=True, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=50, null=True, blank=True)
    phone_number = models.CharField(_("Phone Number"), max_length=10, unique=True)
    photo = models.ImageField(_("Photo"), upload_to='photos', null=True, blank=True)
    is_staff = models.BooleanField(_("Staff"), default=False)
    is_active = models.BooleanField(_("Active"), default=False)
    date_joined = models.DateTimeField(_("Date Joined"), default=timezone.now)
    type=models.CharField(_("User Type"), max_length=50, choices=UserTypes.choices, default=UserTypes.rider)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()        

    def __str__(self):
        return f'{self.phone_number} - {self.type} - {self.id}'
    
#### CREATE PROXY MODELS ####
class Owner(User):
    '''
    Create Owner using a proxy model by inheriting User model
    '''
    
    owners = OwnerManager()

    class Meta:
        proxy = True
    
    def save(self, *args, **kwargs):
        # allow taxi owner to access admin site
        self.is_staff = True

        # if no user exist, set default type
        if not self.pk:
            self.type = User.Types.OWNER
        return super().save(*args, **kwargs)

class Driver(User):
    '''
    Create Driver using a proxy model by inheriting User model
    '''
    
    drivers = DriverManager()

    class Meta:
        proxy = True
    
    def save(self, *args, **kwargs):

        # if no user exist, set default type
        if not self.pk:
            self.type = User.Types.DRIVER
        return super().save(*args, **kwargs)

class Rider(User):
    '''
    Create Rider using a proxy model by inheriting User model
    '''
    
    riders = RiderManager()

    class Meta:
        proxy = True
    
    def save(self, *args, **kwargs):

        # if no user exist, set default type
        if not self.pk:
            self.type = User.Types.RIDER
        return super().save(*args, **kwargs)
