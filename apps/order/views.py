from apps.lib.views import ViewSet
from .models import OrderBase, OrderComment, OrderFile, OrderNumber
from account.models import Account
from number.models import Number
from .serializers import OrderNumberSerializer, OrderSerializer, CommentSerializer, OrderFileSerializer, \
    OrderPortSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import parsers, renderers, status
import uuid
from django.conf import settings
from django.db import transaction
from django.urls import get_script_prefix
from django.utils.encoding import (uri_to_iri)
from urllib.parse import urlparse
from apps.lib.utils import get_pagination, slicer
import requests
import json
from apps.decorators.permission_decorators import require_permissions


class OrderNumberView(ViewSet):

    # Create order with account
    @transaction.atomic
    def create(self, request, id):
        number_url = request.data.get('number')

        number = self.to_internal_value(Number, number_url)
        print(number.e164)
        account = self.get_object_or_404(Account, id)

        headers = {
            'content-type': 'application/json',
            'Authorization': settings.BANDWIDTH_AUTHORIZATION
        }
        data = {
            'number': number.e164,
            'name': '',
            "fallbackNumber": ''
        }
        url = 'https://api.catapult.inetwork.com/v1/users/u-lo5ohxwr4j3mro2vkmzcrka/phoneNumbers'
        order_number = requests.post(url, data=json.dumps(data), headers=headers,
                                     auth=(settings.BANDWIDTH_API_TOKEN, settings.BANDWIDTH_API_SECRETE_KEY))
        if order_number.status_code != 201:
            response = json.loads(order_number.content.decode('utf-8'))
            return Response({'error': response['message']}, status=status.HTTP_400_BAD_REQUEST)

        request.data._mutable = True
        request.data['account'] = account
        request.data['number'] = number
        serializer = OrderNumberSerializer(data=request.data,
                                           context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleOrderNumberView(ViewSet):

    # get single ordernumber informations
    def retrieve(self, request, id, format=None):
        order_number = get_object_or_404(OrderNumber, pk=id)
        serializer = OrderNumberSerializer(order_number, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllOrderView(ViewSet):
    serializer_class = OrderSerializer

    # get paginated all orders informations lists, access for SUPER_ADMIN
    def get_queryset(self):
        orders = OrderBase.objects.all().order_by('-created_at')
        return orders

    def get_serializer_context(self):
        return {'request': self.request}


class SingleAccountOrderView(ViewSet):
    serializer_class = OrderSerializer

    # get paginated all orders informations lists for a indevidual account(id), access for SUPER_ADMIN
    @require_permissions(model=Account)
    def get_queryset(self):
        id = self.kwargs.get('id')
        account = self.get_object_or_404(Account, id)
        request = self.request
        orders = OrderBase.objects.filter(account=account).order_by('-created_at')
        return orders

    def get_serializer_context(self):
        return {'request': self.request}


class SingleOrderView(ViewSet):

    # get single order informations
    def retrieve(self, request, id, format=None):
        order = get_object_or_404(OrderBase, pk=id)
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCommentView(ViewSet):
    serializer_class = CommentSerializer

    # create comments with existing OrderBase id
    def create(self, request, id):
        order = get_object_or_404(OrderBase, pk=id)
        request.data._mutable = True
        request.data['order'] = order

        serializer = CommentSerializer(data=request.data,
                                       context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    # get list of serialized comments_data for single order
    def get_queryset(self):
        id = self.kwargs.get('id')
        order = get_object_or_404(OrderBase, pk=id)
        comments = OrderComment.objects.filter(order=order)
        return comments

    def get_serializer_context(self):
        return {'request': self.request}


class OrderFileView(ViewSet):
    serializer_class = OrderFileSerializer

    # post new file and save
    def create(self, request, id, format=None):
        order = get_object_or_404(OrderBase, pk=id)
        request.data._mutable = True
        request.data['order'] = order

        file = request.FILES.get('file')
        request.data['file'] = file

        serializer = OrderFileSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    # get paginated all orders files lists, access for SUPER_ADMIN
    def get_queryset(self):
        id = self.kwargs.get('id')
        order = get_object_or_404(OrderBase, pk=id)
        order_files = OrderFile.objects.filter(order=order).order_by('-created_at')
        return order_files

    def get_serializer_context(self):
        return {'request': self.request}


class SingelOrderFileView(ViewSet):

    # get single file infomations
    def retrieve(self, request, id, format=None):
        orderfile = get_object_or_404(OrderFile, pk=id)
        serializer = OrderFileSerializer(
            orderfile,
            context={'request': request}
        )
        return Response(serializer.data, status.HTTP_200_OK)


class OrderPortView(ViewSet):
    @transaction.atomic
    @require_permissions(model=Account)
    def create(self, request, id, format=None):
        account = self.get_object_or_404(Account, id)

        request.data._mutable = True
        request.data['account'] = account

        serializer = OrderPortSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BandwidthAvailableNumbersView(ViewSet):
    # E.164 Format ==> +14155552671
    def create(self, request):
        zip = request.data.get('zip')
        quantity = request.data.get('quantity', 5)
        if zip == '' or quantity == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        headers = {
            'content-type': 'application/json',
            'Authorization': settings.BANDWIDTH_AUTHORIZATION
        }
        url = 'https://api.catapult.inetwork.com/v1/availableNumbers/local?zip=' + zip + '&quantity=' + str(quantity)

        numbers = requests.get(url, data={}, headers=headers,
                               auth=(settings.BANDWIDTH_API_TOKEN, settings.BANDWIDTH_API_SECRETE_KEY))
        if numbers.status_code == 200:
            available_numbers = json.loads(numbers.content.decode('utf-8'))
            return Response(available_numbers, status=status.HTTP_200_OK)
        else:
            response = json.loads(numbers.content.decode('utf-8'))
            return Response({'error': response['message']}, status=status.HTTP_400_BAD_REQUEST)
