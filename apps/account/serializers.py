from .models import Account, E911
from django.conf import settings
from rest_framework import status, serializers
import json
from django.http import HttpResponse
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
import uuid
from rest_framework.authtoken.models import Token
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.compat import authenticate
from django.db import transaction
import requests
from .service import get_okta_user_info
from okta.models import OktaUserInfo


class AccountSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(AccountSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.request = kwargs['context']['request']

    _links = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ('id', 'name', 'description',
                  'enabled', 'created_at', '_links')
        read_only_fields = ('created_at',)

    def get__links(self, obj):
        # base = self.context['request'].build_absolute_uri('/')
        base = settings.ABSULATE_API_URL
        _links = {}

        _self = base + '/api/v1/accounts/' + str(obj.id)
        accountNumbers = base + '/api/v1/accounts/' + str(obj.id) + '/numbers'
        accountServers = base + '/api/v1/accounts/' + str(obj.id) + '/servers'

        self_href = {}
        self_href['href'] = _self

        accountNumbers_href = {}
        accountNumbers_href['href'] = accountNumbers

        accountServers_href = {}
        accountServers_href['href'] = accountServers

        _links['self'] = self_href
        _links['accountNumbers'] = accountNumbers_href
        _links['accountServers'] = accountServers_href
        return _links

    @transaction.atomic
    def create(self, valid_data):
        initial_data = self.initial_data
        userid = self.context.get('userid')

        # Here adding info to user

        account = Account(**valid_data)
        account.save()

        try:
            # Getting previous info
            previous_info_response = get_okta_user_info(userid)

            if previous_info_response is False:
                raise serializers.ValidationError({'non_field_errors': ['User info not found on Okta.Something went wrong!']},
                                                  status.HTTP_400_BAD_REQUEST)

            previous_info_response_data = previous_info_response

            url = settings.OKTA_BASE_URL + '/api/v1/apps/' + settings.OKTA_CLIENT_ID + '/users/' + userid
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "SSWS " + settings.API_TOKEN
            }

            arr = []
            previous_group_roles = previous_info_response_data['profile']['group_role']

            if previous_group_roles is not None or previous_group_roles == []:
                for role in previous_group_roles:
                    arr.append(role)
            new_role = str(account.id) + ":admin"
            arr.append(new_role)

            payload = {
                "profile": {
                    "group_role": arr
                }
            }
            response = requests.post(url, data=json.dumps(payload), headers=headers)


            # Update profile start
            update_url = settings.OKTA_BASE_URL + '/api/v1/users/' + userid
            update_headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "SSWS " + settings.API_TOKEN
            }
            update_payload = {
                "profile": {
                    "organization": account.name
                }
            }

            update_response = requests.post(update_url, data=json.dumps(update_payload), headers=update_headers)
            # Update profile end

        except:
            raise serializers.ValidationError({'non_field_errors': ['Something went wrong. Please Try again.']},
                                              status.HTTP_400_BAD_REQUEST)

        return account

    def validate(self, data):
        data = super(AccountSerializer, self).validate(data)
        return data


