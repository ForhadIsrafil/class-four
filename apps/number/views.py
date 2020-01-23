from rest_framework.views import APIView
from rest_framework import status

from apps.decorators.permission_decorators import require_permissions
from .models import Number
from .serializers import NumberSerializer, AccountNumberSerializer, GetAccountNumberSerializer, LidbSerializer, \
    E911Serializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import parsers, renderers, status
import json
from django.db import transaction
from account.models import Account, AccountNumber, Lidb, E911
from django.urls import get_script_prefix
from django.utils.encoding import (uri_to_iri)
from urllib.parse import urlparse
from apps.lib.views import ViewSet
from apps.lib.utils import get_pagination, slicer
from django.conf import settings
from rest_framework import viewsets
from django.db.models import Q
import requests


class NumberView(viewsets.ModelViewSet):
    serializer_class = NumberSerializer

    # Create Number resource (superadmin)
    def create(self, request):
        serializer = NumberSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        is_available = self.request.query_params.get('is_available')

        numbers = Number.objects.all()

        if is_available == '1':
            used_number_ids = AccountNumber.objects.all().values_list('number_id', flat=True)
            numbers = numbers.filter(~Q(id__in=used_number_ids))

        if keyword is not None:
            trimed_keyword = keyword.strip()
            numbers = numbers.filter(e164__icontains=trimed_keyword)

        return numbers


class SingleNumberView(ViewSet):

    # return single Number data for request of e164-number
    def retrieve(self, request, e164_id, format=None):
        number = self.get_object_or_404(Number, e164_id)
        serializer = NumberSerializer(number, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # update single Number, based on Numbers e164-number(as id)
    def partial_update(self, request, e164_id):
        instance = self.get_object_or_404(Number, e164_id)
        serializer = NumberSerializer(instance,
                                      data=request.data,
                                      partial=True,
                                      context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Delete single number using e164-number
    def destroy(self, request, e164_id):
        number = self.get_object_or_404(Number, e164_id)
        number.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountNumberView(ViewSet):
    serializer_class = GetAccountNumberSerializer

    # Creating AccountNumber resource that assigns a number to an account
    @require_permissions(model=Account)
    @transaction.atomic
    def create(self, request, id):
        number_url = request.POST.get('number')
        number = self.to_internal_value(Number, number_url)

        account = self.get_object_or_404(Account, id)

        serializer = AccountNumberSerializer(data=request.data,
                                             context={'account': account, 'number': number, 'request': request})

        if serializer.is_valid():

            url = settings.MESSAGE_API_URL + '/number'
            hesders = {
                "Content-Type": "application/json",
                "Authorization": request.META.get('HTTP_AUTHORIZATION')
            }
            data = {"number": number.e164}
            create_message_api_number_response = requests.post(url, data=json.dumps(data), headers=hesders)
            if create_message_api_number_response.status_code == 201:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                response = json.loads(create_message_api_number_response.content.decode('utf-8'))
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @require_permissions(model=Account)
    def get_queryset(self):
        id = self.kwargs.get('id')
        account = self.get_object_or_404(Account, id)
        account_numbers = AccountNumber.objects.filter(account=account).order_by('-created_at').all()
        return account_numbers

    def get_serializer_context(self):
        return {'request': self.request}


class SingleAccountNumberView(ViewSet):

    # Get single account number information
    def retrieve(self, request, id, format=None):
        accountnumber = self.get_object_or_404(AccountNumber, id)
        serializer = GetAccountNumberSerializer(
            accountnumber,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountNumberLidbView(ViewSet):
    serializer_class = LidbSerializer

    # Idempotent LIDB create here
    def update(self, request, id, format=None):
        accountnumber = self.get_object_or_404(AccountNumber, id)

        name = request.data.get('name')
        kind = request.data.get('kind')

        if None in [name, kind]:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        lidb = Lidb(accountnumber=accountnumber, name=name, kind=kind)
        lidb.save()

        serializer = LidbSerializer(
            lidb,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Getting all lidb for an account with paginated view
    def get_queryset(self):
        id = self.kwargs.get('id')
        accountnumber = self.get_object_or_404(AccountNumber, id)
        lidbs = Lidb.objects.filter(accountnumber=accountnumber)
        return lidbs

    def get_serializer_context(self):
        return {'request': self.request}


class E911View(ViewSet):
    serializer_class = E911Serializer

    # get AccountNumber id and update(put) E911
    def update(self, request, id):
        accountnumber = self.get_object_or_404(AccountNumber, id)

        request.data._mutable = True
        request.data['accountnumber'] = accountnumber.id

        serializer = E911Serializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Getting all E911 for an account with paginated view
    def get_queryset(self):
        id = self.kwargs.get('id')
        accountnumber = self.get_object_or_404(AccountNumber, id)
        e911s = E911.objects.filter(accountnumber=accountnumber)
        return e911s

    def get_serializer_context(self):
        return {'request': self.request}


class ManualCreateNumber(ViewSet):
    def create(self, request):
        source_list = open(settings.SYSTEM_NUMBERS_FILE_PATH)
        source_numbers = source_list.read().split(', ')

        for e164 in source_numbers:
            e164 = e164.replace('(', '').replace(')', '').replace('-', '')
            number = Number(e164=e164, status='portedin')
            number.save()

        return Response(status=status.HTTP_200_OK)
