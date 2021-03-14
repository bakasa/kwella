from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _ 
from django.utils import timezone
from .managers import CustomUserManager, DriverManager, OwnerManager, RiderManager

class User(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        DRIVER = ('DRIVER', 'driver')
        OWNER = ('OWNER', 'owner')
        RIDER = ('RIDER', 'rider')

    phone_number = models.IntegerField(_("Phone Number"), unique=True)
    is_staff = models.BooleanField(_("Staff"), default=False)
    is_active = models.BooleanField(_("Active"), default=False)
    date_joined = models.DateTimeField(_("Date Joined"), default=timezone.now)
    type=models.CharField(_("User Type"), max_length=50, choices=Types.choices, default=Types.RIDER)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.phone_number} - {self.type}'
    
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
