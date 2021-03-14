from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _ 
from django.utils import timezone

class User(AbstractBaseUser, PermissionsMixin):
    pass
