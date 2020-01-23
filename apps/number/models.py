import uuid
from datetime import datetime
from django.db import models


class Number(models.Model):
    PORTED_IN = 'portedin'
    PORTED_OUT = 'portedout'
    PORTING_IN = 'portingin'
    PORTING_OUT = 'portingout'
    DISABLED = 'disabled'

    STATUS_CHOICES = (
        (PORTED_IN, 'Ported In'),
        (PORTED_OUT, 'Ported Out'),
        (PORTING_IN, 'Porting In'),
        (PORTING_OUT, 'Porting Out'),
        (DISABLED, 'Disabled'),
        )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )

    e164 = models.CharField(
        max_length=15,
        unique=True
        )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PORTED_IN
        )

    class Meta:
        db_table = 'number'


