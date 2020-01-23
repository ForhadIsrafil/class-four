from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status
from .models import AccountNumber, Account, AccountServer, E911
from .serializers import AccountSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import parsers, renderers, status
import json
from django.db import transaction
from .utils import slicer
from django.shortcuts import get_object_or_404
from apps.lib.views import ViewSet
from apps.lib.utils import get_pagination, Mailer
from django.conf import settings
import requests
from okta.models import OktaUserInfo
from .service import get_okta_user_info, get_okta_user_profile_with_organization_info
from rest_framework import viewsets
from apps.decorators.permission_decorators import require_permissions


class AccountView(ViewSet):
    serializer_class = AccountSerializer

    # create a new account by giving name and description which is optional(main is the uuid)
    @transaction.atomic
    def create(self, request):

        serializer = AccountSerializer(
            data=request.data,
            context={'request': request, 'userid': request.user.oktauserinfo.okta_user_id}
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # list of paginated all Account data, showing base on updated created date and time
    def get_queryset(self):
        accounts = Account.objects.all().order_by('-created_at')
        return accounts

    def get_serializer_context(self):
        return {'request': self.request}

    # representing single account data(informations) for requested account id
    @require_permissions(model=Account)
    def retrieve(self, request, id, format=None):
        account = self.get_object_or_404(Account, id)

        serializer = AccountSerializer(account, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    # update the existing information of a single account
    @require_permissions(model=Account)
    def partial_update(self, request, id):
        instance = self.get_object_or_404(Account, id)

        allow_request = self.check_account_object_permissions(request, instance)
        if allow_request:
            serializer = AccountSerializer(instance,
                                           data=request.data,
                                           partial=True,
                                           context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    # delete the valid account informations
    @transaction.atomic
    @require_permissions(model=Account)
    def destroy(self, request, id):
        account = self.get_object_or_404(Account, id)

        account.accountserver_set.all().delete()
        for accountnumber in account.accountnumber_set.all():
            accountnumber.lidb_set.all().delete()
            accountnumber.e911_set.all().delete()
        account.accountnumber_set.all().delete()

        for order in account.orderbase_set.all():
            order.orderfile_set.all().delete()
            order.ordernumber_set.all().delete()
            order.ordercomment_set.all().delete()
            order.orderport_set.all().delete()

        for route in account.route_set.all():
            route.server_set.all().delete()

        account.route_set.all().delete()
        account.orderbase_set.all().delete()
        account.delete()

        sid = transaction.savepoint()

        # now reset the user info
        okta_user_id = OktaUserInfo.objects.get(user_id=request.user.id).okta_user_id
        url = settings.OKTA_BASE_URL + '/api/v1/apps/' + settings.OKTA_CLIENT_ID + '/users/' + str(okta_user_id)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "SSWS " + settings.API_TOKEN
        }
        arr = []
        user_info = OktaUserInfo.objects.get(user=request.user)
        okta_user = get_okta_user_info(user_info.okta_user_id)
        previous_group_roles = okta_user['profile']['group_role']

        if previous_group_roles is not None or previous_group_roles == []:
            for role in previous_group_roles:
                arr.append(role)

        deleted_info = str(id) + ":admin"
        arr.remove(deleted_info)
        payload = {
            "profile": {
                "group_role": arr
            }
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response_data = response.json()

        self.request.session.modified = True
        self.request.session["okta_user"] = response_data

        transaction.savepoint_commit(sid)

        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckFamilyNameAvailability(ViewSet):
    @transaction.atomic
    def check(self, request, format=None):
        family_name = request.data.get('family_name')
        is_exists = Account.objects.filter(name=family_name).exists()

        res = False
        if not is_exists:
            res = True

        response = {
            'allow': res
        }
        return Response(response, status=status.HTTP_200_OK)


class GetAccountInfoView(ViewSet):
    @transaction.atomic
    def list(self, request, format=None):

        # collecting account infos
        okta_user_info = get_okta_user_info(request.user.oktauserinfo.okta_user_id)

        if not okta_user_info:
            return Response({'error': 'We Could not found your group role information. Something must wrong .'},
                            status=status.HTTP_400_BAD_REQUEST)

        arr = []
        previous_group_roles = okta_user_info['profile']['group_role']

        if previous_group_roles is not None or previous_group_roles == []:
            for role in previous_group_roles:
                arr.append(role)

        response = {
            'data': arr
        }
        return Response(response, status=status.HTTP_200_OK)
