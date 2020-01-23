import uuid
from datetime import datetime
from django.utils import timezone
from django.db import models
from account.models import Account
from number.models import Number


class OrderBase(models.Model):

    PENDING = 'pending'
    COMPLETE = 'complete'
    CANCELED = 'canceled'
    REJECTED = 'rejected'

    STATUS_CHOICES = (
        (PENDING, 'pending'),
        (COMPLETE, 'complete'),
        (CANCELED, 'canceled'),
        (REJECTED, 'rejected'),
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    kind = models.CharField(null=True, max_length=50)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'order'


class OrderFile(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    order = models.ForeignKey(OrderBase, on_delete=models.PROTECT)
    description = models.TextField()
    kind = models.TextField()
    file_name = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'order_file'

class OrderComment(models.Model):
    order = models.ForeignKey(OrderBase, on_delete=models.PROTECT)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'order_comment'


class OrderNumber(models.Model):
    order = models.ForeignKey(OrderBase, on_delete=models.PROTECT)
    number = models.ForeignKey(Number, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now)


    class Meta:
        db_table = 'order_number'

class OrderPort(models.Model):

    PARTIAL = 'partial'
    FULL = 'full'


    PENDING = 'pending'
    FOC = 'foc'
    REJECTED = 'rejected'


    TYPE_CHOICES = (
        (PARTIAL, 'partial'),
        (FULL, 'full')
    )


    STATE_CHOICES = (
        (PENDING, 'pending'),
        (FOC, 'foc'),
        (REJECTED, 'rejected')
    )

    order = models.ForeignKey(OrderBase, on_delete=models.PROTECT)
    e164 = models.CharField(
        max_length=15,
        unique=True
        )
    port_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default=PARTIAL
    )

    ddd = models.DateTimeField(default=timezone.now)
    btn = models.CharField(max_length=50)
    name = models.TextField()
    authorizer = models.TextField()
    address1 = models.TextField()
    address2 = models.TextField()
    city = models.TextField()
    state = models.CharField(
        max_length=50,
        choices=STATE_CHOICES,
        default=PENDING
    )
    zip = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)


    class Meta:
        db_table = 'order_port'