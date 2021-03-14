from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _ 
from django.utils import timezone

class User(AbstractUser):
    pass
