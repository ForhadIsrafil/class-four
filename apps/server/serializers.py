from .models import Server, Route
from account.models import AccountServer, Account
from django.conf import settings
from rest_framework import serializers
from rest_framework import status
import json
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
import uuid
from rest_framework.authtoken.models import Token
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.compat import authenticate
from django.db import transaction


class RouteSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(RouteSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.request = kwargs['context']['request']

    account = serializers.SerializerMethodField()
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = ('id', 'name', 'account',
                  '_links'
                  )

    @transaction.atomic
    def create(self, valid_data):
        initial_data = self.initial_data

        name = initial_data['name']
        account = initial_data['account']

        # saving route
        route = Route(name=name,
                      account=account
                      )
        route.save()
        return route

    def get__links(self, obj):
        base = settings.ABSULATE_API_URL
        _links = {}
        _self = base + '/api/v1/routes/' + str(obj.id)
        self_href = {}
        self_href['href'] = _self
        _links['self'] = self_href
        return _links

    def get_account(self, obj):
        base = settings.ABSULATE_API_URL
        url = base + '/api/v1/accounts/' + str(obj.account.id)
        return url


class ServerSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(ServerSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.request = kwargs['context']['request']

    _links = serializers.SerializerMethodField()
    route = serializers.SerializerMethodField()

    class Meta:
        model = Server
        fields = ('id', 'uri', 'weight',
                  'priority', 'socket', 'state',
                  'attrs', 'algorithm', 'name',
                  'description', 'kind', 'host',
                  'port', 'transport', 'channels',
                  'enabled', 'route', '_links'
                  )
        extra_kwargs = {
            'route': {'write_only': True},
            'socket': {'write_only': True},
            'state': {'write_only': True},
            'attrs': {'write_only': True},
            'enabled': {'write_only': True},
            'kind': {'write_only': True},
        }

    @transaction.atomic
    def create(self, valid_data):
        initial_data = self.initial_data

        uri = initial_data['uri']
        weight = initial_data['weight']
        priority = initial_data['priority']
        socket = initial_data['socket']
        state = initial_data['state']
        attrs = initial_data['attrs']
        algorithm = initial_data['algorithm']
        name = initial_data['name']
        description = initial_data['description']
        kind = initial_data['kind']
        host = initial_data['host']
        port = initial_data['port']
        transport = initial_data['transport']
        channels = initial_data['channels']
        enabled = initial_data.get('enabled', True)

        route = initial_data['route']

        # saving server
        server = Server(uri=uri,
                        weight=weight,
                        priority=priority,
                        socket=socket,
                        state=state,
                        attrs=attrs,
                        algorithm=algorithm,
                        name=name,
                        description=description,
                        kind=kind,
                        host=host,
                        port=port,
                        transport=transport,
                        channels=channels,
                        enabled=enabled,
                        route=route
                        )

        server.save()
        return server

    def validate(self, data):
        data = super(ServerSerializer, self).validate(data)
        return data

    def get__links(self, obj):
        base = settings.ABSULATE_API_URL
        _links = {}
        _self = base + '/api/v1/servers/' + str(obj.id)
        self_href = {}
        self_href['href'] = _self
        _links['self'] = self_href
        return _links

    def get_route(self, obj):
        base = settings.ABSULATE_API_URL
        url = base + '/api/v1/routes/' + str(obj.route.id)
        return url
