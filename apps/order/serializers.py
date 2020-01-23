from .models import OrderFile, OrderComment, OrderBase, OrderNumber, OrderPort
from django.conf import settings
from rest_framework import status
import json
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
import tempfile
import shutil
import uuid
from rest_framework.authtoken.models import Token
import os
from rest_framework import serializers
from rest_framework.compat import authenticate
from django.db import transaction


class OrderNumberSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(OrderNumberSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.request = kwargs['context']['request']

    _links = serializers.SerializerMethodField()
    number = serializers.SerializerMethodField()
    kind = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    account = serializers.SerializerMethodField()

    class Meta:
        model = OrderNumber
        fields = ('id', 'number', 'account', 'created_at', 'status', 'kind', '_links')
        read_only_fields = ('created_at',)

    def get_number(self, obj):
        base = settings.ABSULATE_API_URL
        number_url = base + '/api/v1/numbers/' + str(obj.number.e164)
        return number_url

    def get_kind(self, obj):
        return obj.order.kind

    def get_status(self, obj):
        return obj.order.status

    def get_account(self, obj):
        base = settings.ABSULATE_API_URL
        account_url = base + '/api/v1/accounts/' + str(obj.order.account.id)
        return account_url

    def get__links(self, obj):
        base = settings.ABSULATE_API_URL
        _links = {}

        _self = base + '/api/v1/ordernumbers/' + str(obj.id)
        order = base + '/api/v1/orders/' + str(obj.order.id)
        files = base + '/api/v1/orders/' + str(obj.order.id) + '/files'
        comments = base + '/api/v1/orders/' + str(obj.order.id) + '/comments'

        self_href = {}
        self_href['href'] = _self

        order_href = {}
        order_href['href'] = order

        files_href = {}
        files_href['href'] = files

        comments_href = {}
        comments_href['href'] = comments

        _links['self'] = self_href
        _links['order'] = order_href
        _links['files'] = files_href
        _links['comments'] = comments_href
        return _links

    @transaction.atomic
    def create(self, valid_data):
        initial_data = self.initial_data
        order = OrderBase(kind='number', account=initial_data['account'])
        order.save()

        order_number = OrderNumber(order=order, number=initial_data['number'])
        order_number.save()
        return order_number

    def validate(self, data):
        data = super(OrderNumberSerializer, self).validate(data)
        return data


class OrderSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(OrderSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.request = kwargs['context']['request']

    _links = serializers.SerializerMethodField()
    account = serializers.SerializerMethodField()

    class Meta:
        model = OrderBase
        fields = ('id', 'status', 'kind', 'account', 'created_at', '_links')

    # build links for represent nore data
    def get__links(self, obj):
        base = settings.ABSULATE_API_URL

        _links = {}
        _self = base + '/api/v1/orders/' + str(obj.id)
        _account = base + '/api/v1/accounts/' + str(obj.account.id)

        self_href = {}
        account_href = {}

        self_href['href'] = _self
        account_href['href'] = _account

        _links['self'] = self_href
        _links['account'] = account_href

        return _links

    def get_account(self, obj):
        base = settings.ABSULATE_API_URL
        account_url = base + '/api/v1/accounts/' + str(obj.account.id)
        return account_url


class CommentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CommentSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.request = kwargs['context']['request']

    _links = serializers.SerializerMethodField()

    class Meta:
        model = OrderComment
        fields = ('id', 'text', 'created_at', '_links')

    # create and save orders comments
    def create(self, valid_data):
        initial_data = self.initial_data
        text = initial_data['text']
        order = initial_data['order']
        order_comment = OrderComment(text=text, order=order)
        order_comment.save()
        return order_comment

    def get__links(self, obj):
        base = settings.ABSULATE_API_URL
        _links = {}
        ordercomments = base + '/api/v1/orders/' + str(obj.order.id) + '/comments'
        ordercomments_href = {}
        ordercomments_href['href'] = ordercomments
        _links['ordercomments'] = ordercomments_href

        return _links


class OrderFileSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(OrderFileSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.request = kwargs['context']['request']

    _links = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = OrderFile
        fields = ('id', 'description', 'kind', 'url', 'created_at', '_links')

    def get__links(self, obj):
        base = settings.ABSULATE_API_URL

        _links = {}
        _self = base + '/api/v1/orderfiles/' + str(obj.id)
        _orders = base + '/api/v1/orders/' + str(obj.order.id)

        self_href = {}
        orders_href = {}

        self_href['href'] = _self
        orders_href['href'] = _orders

        _links['self'] = self_href
        _links['order'] = orders_href

        return _links

    def get_url(self, obj):
        base = settings.ABSULATE_API_URL
        url = base + '/api/v1/media/file/' + str(obj.file_name)
        return url

    # create and save orders files
    def create(self, valid_data):
        initial_data = self.initial_data
        description = initial_data['description']
        kind = initial_data['kind']
        order = initial_data['order']
        file = initial_data['file']

        try:
            hash = str(uuid.uuid4())
            # Process the uploaded model
            _, ext = os.path.splitext(file.name)
            type = ext[1:].lower() if len(ext) > 0 else None

            with tempfile.NamedTemporaryFile(delete=False) as fp:  # creating temporary files
                tmppath = fp.name
                for chunk in file.chunks():
                    fp.write(chunk)

                # Save the model in the static path
                path = settings.FILE_ROOT + '/' + hash + '.' + type
                # utility function for coping and archiving files and directory
                shutil.copyfile(tmppath, path)
                file_name = hash + '.' + type
        except:
            raise serializers.ValidationError({'non_field_errors': ['File is not valid.']},
                                              status.HTTP_400_BAD_REQUEST)

        order_file = OrderFile(description=description, kind=kind, file_name=file_name, order=order)
        order_file.save()
        return order_file


class OrderPortSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(OrderPortSerializer, self).__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            self.request = kwargs['context']['request']

    _links = serializers.SerializerMethodField()
    account = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    kind = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = OrderPort
        fields = ('id', 'account', 'created_at', 'status', 'kind', 'ddd', 'btn', 'e164', '_links')
        extra_kwargs = {'e164': {'write_only': True}}

    def get_account(self, obj):
        base = settings.ABSULATE_API_URL
        _self = base + '/api/v1/account/' + str(obj.order.account.id)
        return _self

    def get_created_at(self, obj):
        return obj.created_at

    def get_status(self, obj):
        return obj.order.status

    def get_kind(self, obj):
        return obj.order.kind

    def get__links(self, obj):
        base = settings.ABSULATE_API_URL

        _links = {}
        _self = base + '/api/v1/orderports/' + str(obj.id)
        _orders = base + '/api/v1/orders/' + str(obj.order.id)
        _files = base + '/api/v1/orders/'+str(obj.order.id)+'/files'
        _comments = base + '/api/v1/orders/'+str(obj.order.id)+'/comments'

        self_href = {}
        orders_href = {}
        files_href = {}
        comments_href = {}

        self_href['href'] = _self
        orders_href['href'] = _orders
        files_href['href'] = _files
        comments_href['href'] = _comments

        _links['self'] = self_href
        _links['order'] = orders_href
        _links['files'] = files_href
        _links['comments'] = comments_href

        return _links

    @transaction.atomic
    def create(self, valid_data):
        initial_data = self.initial_data
        account = initial_data.get('account')
        kind = initial_data.get('kind')
        e164 = initial_data.get('e164')
        port_type = initial_data.get('port_type')
        authorizer = initial_data.get('authorizer')
        address1 = initial_data.get('address1')
        address2 = initial_data.get('address2')
        city = initial_data.get('city')
        state = initial_data.get('state')
        zip = initial_data.get('zip')
        name = initial_data.get('name')
        btn = initial_data.get('btn')

        order = OrderBase(kind=kind, account=account)
        order.save()

        order_port = OrderPort(e164=e164, port_type=port_type, name=name, authorizer=authorizer,
                               address1=address1, address2=address2, city=city, btn=btn,
                               state=state, zip=zip, order=order
                               )
        order_port.save()
        return order_port

    def validate(self, data):
        data = super(OrderPortSerializer, self).validate(data)
        return data
