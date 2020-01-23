from .models import Number
from account.models import AccountNumber, Account, Lidb, E911
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
import requests
from django.http import Http404
import requests


class NumberSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(NumberSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.request = kwargs['context']['request']

    _links = serializers.SerializerMethodField()

    class Meta:
        model = Number
        fields = ('id', 'e164', 'status', '_links')

    @transaction.atomic
    def create(self, valid_data):
        initial_data = self.initial_data

        e164 = initial_data['e164']
        status = initial_data.get('status', 'portedin')  # optional
        # saving number
        number = Number(e164=e164, status=status)
        number.save()
        return number

    def validate(self, data):
        data = super(NumberSerializer, self).validate(data)
        return data

    def get__links(self, obj):
        base = settings.ABSULATE_API_URL
        _links = {}
        _self = base + '/api/v1/numbers/' + str(obj.e164)
        self_href = {}
        self_href['href'] = _self
        _links['self'] = self_href
        return _links


class AccountNumberSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(AccountNumberSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.request = kwargs['context']['request']
            self.account = kwargs['context']['account']
            self.number_obj = kwargs['context']['number']

    _links = serializers.SerializerMethodField()
    account = serializers.SerializerMethodField()
    number = serializers.SerializerMethodField()

    class Meta:
        model = AccountNumber
        fields = ('id', 'account', 'number', 'created_at', '_links')

    @transaction.atomic
    def create(self, valid_data):
        account_number = AccountNumber(account=self.account, number=self.number_obj)
        account_number.save()

        return account_number

    def get__links(self, obj):
        base = settings.ABSULATE_API_URL
        _links = {}
        _self = base + '/api/v1/accountnumbers/' + str(obj.id)
        _lidb = base + '/api/v1/accountnumbers/' + str(obj.id) + '/lidb'
        _e911 = base + '/api/v1/accountnumbers/' + str(obj.id) + '/e911'

        self_href = {}
        self_href['href'] = _self

        lidb_href = {}
        lidb_href['href'] = _lidb

        e911_href = {}
        e911_href['href'] = _e911

        _links['self'] = self_href
        _links['lidb'] = lidb_href
        _links['e911'] = e911_href

        return _links

    def get_account(self, obj):
        base = settings.ABSULATE_API_URL
        url = base + '/api/v1/accounts/' + str(obj.account.id)
        return url

    def get_number(self, obj):

        base = settings.ABSULATE_API_URL
        number_url = base + '/api/v1/numbers/' + self.number_obj.e164
        return number_url

    def validate(self, validated_data):

        if AccountNumber.objects.filter(account=self.account, number=self.number_obj).exists():
            raise serializers.ValidationError({'non_field_errors': ['Account with this number already exists.']},
                                              status.HTTP_400_BAD_REQUEST)
        data = super(AccountNumberSerializer, self).validate(validated_data)
        return data


class GetAccountNumberSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(GetAccountNumberSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.request = kwargs['context']['request']

    _links = serializers.SerializerMethodField()
    account = serializers.SerializerMethodField()
    number = serializers.SerializerMethodField()

    class Meta:
        model = AccountNumber
        fields = ('id', 'account', 'number', 'created_at', '_links')

    def get__links(self, obj):
        base = settings.ABSULATE_API_URL
        _links = {}
        _self = base + '/api/v1/accountnumbers/' + str(obj.id)
        _lidb = base + '/api/v1/accountnumbers/' + str(obj.id) + '/lidb'
        _e911 = base + '/api/v1/accountnumbers/' + str(obj.id) + '/e911'

        self_href = {}
        self_href['href'] = _self

        lidb_href = {}
        lidb_href['href'] = _lidb

        e911_href = {}
        e911_href['href'] = _e911

        _links['self'] = self_href
        _links['lidb'] = lidb_href
        _links['e911'] = e911_href

        return _links

    def get_account(self, obj):
        base = settings.ABSULATE_API_URL
        url = base + '/api/v1/accounts/' + str(obj.account.id)
        return url

    def get_number(self, obj):
        base = settings.ABSULATE_API_URL
        url = base + '/api/v1/numbers/' + str(obj.number.e164)
        return url


class LidbSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(LidbSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.request = kwargs['context']['request']

    _links = serializers.SerializerMethodField()

    class Meta:
        model = Lidb
        fields = ('name', 'kind', '_links')

    def get__links(self, obj):
        base = settings.ABSULATE_API_URL
        _links = {}
        _self = base + '/api/v1/accountnumbers/' + str(obj.accountnumber.id) + '/lidb'
        self_href = {}
        self_href['href'] = _self
        _links['self'] = self_href
        return _links


class E911Serializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(E911Serializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.request = kwargs['context']['request']

    _links = serializers.SerializerMethodField()

    class Meta:
        model = E911
        fields = ('id', 'address1', 'address2',
                  'city', 'state', 'zipcode',
                  'zipcode2', 'comment', 'created_at', '_links', 'accountnumber'
                  )
        extra_kwargs = {'accountnumber': {'write_only': True}}

    def get__links(self, obj):
        base = settings.ABSULATE_API_URL
        _links = {}
        _self = base + '/api/v1/accountnumbers/' + str(obj.accountnumber.id) + '/e911'
        self_href = {}
        self_href['href'] = _self
        _links['self'] = self_href
        return _links
