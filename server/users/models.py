import random
from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django_otp.oath import TOTP

from .managers import (CustomUserManager, DriverManager, OwnerManager,
                       RiderManager)


class User(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        DRIVER = ('DRIVER', 'Driver')
        OWNER = ('OWNER', 'Owner')
        RIDER = ('RIDER', 'Rider')

    first_name = models.CharField(_("First Name"), max_length=50, null=True, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=50, null=True, blank=True)
    phone_number = models.CharField(_("Phone Number"), max_length=10, unique=True)
    is_staff = models.BooleanField(_("Staff"), default=False)
    is_active = models.BooleanField(_("Active"), default=False)
    date_joined = models.DateTimeField(_("Date Joined"), default=timezone.now)
    type=models.CharField(_("User Type"), max_length=50, choices=Types.choices, default=Types.RIDER)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    generated_otp = models.IntegerField(_("OTP"), blank=True, null=True)

    objects = CustomUserManager()

    def handle_otp(self, sent_otp=None):
        '''
        If opt_token is None, generate OTP to send to user's phone number. 
        If sent_otp is not None, validate OTP token.
        The generated token expires after 5 minutes if not verified.
        '''
        
        totp = TOTP(key=bytes('settings.SECRET_KEY', encoding='utf-8'), t0=(int(datetime.now(tz=pytz.UTC).timestamp()) - random.randint(10000, 100000)), digits=5, step=300)

        if sent_otp is None:
            # create new otp token
            print(f'\nsent is None: {totp.token()}\n')
            return totp
        
        print(f'\nsent is NOT None: {totp.token()}\n')
        return totp.verify(sent_otp)
        

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
