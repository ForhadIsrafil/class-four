import uuid
from datetime import datetime
from django.db import models
from django.utils import timezone


class ServerBase(models.Model):
    # OpenSIPS dispatcher columns
    uri = models.TextField(unique=True)  # destination_col (sip:<ip|host>:port)
    weight = models.PositiveIntegerField(default=0)  # OpenSIPS weight_col
    priority = models.PositiveIntegerField(default=0)  # OpenSIPS priority_col
    socket = models.CharField(max_length=128)  # OpenSIPS socket_col
    state = models.IntegerField(default=0)  # OpenSIPS state_col (2=ping)
    attrs = models.CharField(max_length=128)  # OpenSIPS attrs_col
    algorithm = models.PositiveIntegerField(default=8)  # dispatcher alg

    # Descriptive
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    kind = models.TextField()  # core,edge,carrier,
    host = models.TextField(blank=True, null=True)  # built from uri?
    port = models.PositiveIntegerField(default=5060)
    transport = models.TextField(default="udp")
    channels = models.PositiveIntegerField(default=0)

    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def enabled_only(self):
        return self.objects.filter(enabled=True)


class Route(models.Model):
    name = models.CharField(max_length=255)
    account = models.ForeignKey('account.account', on_delete=models.PROTECT)

    class Meta:
        db_table = 'route'


class Server(ServerBase):
    route = models.ForeignKey(Route, on_delete=models.PROTECT)

    class Meta:
        db_table = 'server'



