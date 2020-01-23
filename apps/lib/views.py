from rest_framework.viewsets import ViewSet as BaseViewSet
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework import parsers, renderers, status
from django.conf import settings
from django.db import transaction
from django.urls import get_script_prefix
from django.utils.encoding import (uri_to_iri)
from urllib.parse import urlparse
from .utils import slicer
from number.models import Number
from account.service import get_okta_user_info
from okta.models import OktaUserInfo
from rest_framework import viewsets



class ViewSet(viewsets.ModelViewSet):
    def get_object_or_404(self, model, look_up_for):
        # catch invalid uuids
        try:
            if model == Number:
                return model.objects.get(e164=look_up_for)
            else:
                return model.objects.get(pk=look_up_for)
        except:
            raise Http404

    def to_internal_value(self, model, data):
        try:
            http_prefix = data.startswith(('http:', 'https:'))
        except AttributeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if http_prefix:
            # If needed convert absolute URLs to relative path
            data = urlparse(data).path
            prefix = get_script_prefix()
            if data.startswith(prefix):
                data = '/' + data[len(prefix):]
        data = uri_to_iri(data)
        look_up_for = data.split('/')[-1]

        return self.get_object_or_404(model=model, look_up_for=look_up_for)

    # def list(self, request, id):
    #     pass
    #
    # def retrieve(self, request, id, format=None):
    #     pass

    def check_account_object_permissions(self, request, obj):
        account_ids = []
        user_info = OktaUserInfo.objects.get(user=request.user)

        okta_user = get_okta_user_info(user_info.okta_user_id)

        try:
            group_roles = okta_user['profile']['group_role']
            if group_roles is not None or group_roles == []:
                for group_role in group_roles:
                    account_id, role = group_role.split(':')
                    account_ids.append(account_id)

            if str(obj.id) in account_ids:
                return True
            else:
                return False
        except:
            return False


