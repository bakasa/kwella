import random
from datetime import datetime
from django.conf import settings

import pytz
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_otp.oath import TOTP
from sendsms import api
