import uuid
from datetime import datetime
from django.db import models
from django.utils import timezone
from number.models import Number
from server.models import Server


class Account(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.TextField(unique=True)
    description = models.TextField(null=True, blank=True)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'account'


# Number

class AccountNumber(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    """ Relationship Model """
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    number = models.ForeignKey(Number, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'account_number'
        unique_together = ("account", "number")


class Lidb(models.Model):
    RESIDENTIAL = 'residential'
    BUSINESS = 'business'

    STATUS_CHOICES = (
        (RESIDENTIAL, 'Residential'),
        (BUSINESS, 'Business'),
    )

    kind = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default=BUSINESS
    )

    name = models.CharField(max_length=15)
    accountnumber = models.ForeignKey(AccountNumber, on_delete=models.PROTECT)

    class Meta:
        db_table = 'account_number_lidb'


class E911(models.Model):
    address1 = models.TextField()
    address2 = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    zipcode2 = models.CharField(max_length=5, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    accountnumber = models.ForeignKey(AccountNumber, on_delete=models.PROTECT)

    class Meta:
        db_table = 'account_number_e911'


# Server

class AccountServer(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    """ Relationship Model """
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    server = models.ForeignKey(Server, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'account_server'
        unique_together = ("account", "server")
