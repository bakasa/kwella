from django.db import models
from django.utils.translation import gettext_lazy as _


class UserTypes(models.TextChoices):
    driver = (_('DRIVER'), _('Driver'))
    owner = (_('OWNER'), _('Owner'))
    rider = (_('RIDER'), _('Rider'))
