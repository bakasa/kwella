from django.db import models
from django.utils.translation import gettext_lazy as _


class TripStatus(models.TextChoices):
    requested = (_('REQUESTED'), _('requested'))
    started = (_('STARTED'), _('started'))
    in_progress = (_('PROGRESSING'), _('progressing'))
    completed = (_('COMPLETED'), _('completed'))
