from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import Account
from number.models import Number
from order.models import OrderBase, OrderNumber, OrderComment,OrderFile
from django.conf import settings
import json


class OrderTests(APITestCase):

    # import fixtures
    fixtures = ['initial_fixtures.json']

# =============================== order_number =================================

    # create order numbers
    def test_create_order_numbers(self):
        """
        Ensure we can create a new order object.
        """
        id = Account.objects.first().id
        url = reverse('order:order_number', kwargs={'id': id})
        data = {
        "number":"http://127.0.0.1:8000/api/v1/numbers/713000786",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderBase.objects.count(), 8)

    # create order numbers failed
    def test_create_order_numbers_failed(self):
        id = Account.objects.first().id
        url = reverse('order:order_number', kwargs={'id': id})
        data = {
        "number": "http://127.0.0.1:8000/api/v1/numbers/000000",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(OrderBase.objects.count(), 7)

        # create order numbers failed
    def test_create_order_numbers_failed_1(self):
        id = "c8dba44e-bcc8-4515-0000-08f4bc5a3384"
        url = reverse('order:order_number', kwargs={'id': id})
        data = {
        "number": "http://127.0.0.1:8000/api/v1/numbers/713000786",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(OrderBase.objects.count(), 7)

    # create order numbers failed(2 false(id & number_url))
    def test_create_order_numbers_failed_2(self):
        id = "c8dba44e-bcc8-4515-0000-08f4bc5a3384"
        url = reverse('order:order_number', kwargs={'id': id})
        data = {
        "number": "http://127.0.0.1:8000/api/v1/numbers/00000000",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(OrderBase.objects.count(), 7)

# ============================= all_orders =====================================

    # get all orders
    def test_get_all_orders(self):
        url = reverse('order:all_orders')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OrderBase.objects.count(), 7)

# ============================= single_order ===================================

    # retrieve single orders
    def test_get_single_order(self):
        id = OrderBase.objects.first().id
        url = reverse('order:single_order', kwargs={'id': id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # retrieve single orders(failed)
    def test_get_single_order_failed(self):
        id = "8c0f3e2d-db20-48ac-0000-54031de5bca0"
        url = reverse('order:single_order', kwargs={'id': id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# ========================== single_account_orders =============================

    # Get all orders for an Account
    def test_get_single_account_all_orders(self):
        id = Account.objects.first().id
        url = reverse('order:single_account_orders', kwargs={'id': id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # all orders for an Account(failed)[not an existing Account id]
    def test_get_single_account_all_orders_failed(self):
        id = "c8dba44e-bcc8-4515-0000-08f4bc5a3384"
        url = reverse('order:single_account_orders', kwargs={'id': id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# ============================ order_comments ==================================

    # create order comments
    def test_create_order_comments(self):
        id = OrderBase.objects.first().id
        url = reverse('order:order_comments', kwargs={'id': id})
        data = {
        "text": "first text here......."
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderComment.objects.count(), 20)

    # create order comment failed
    def test_create_order_comments_failed(self):
        id = OrderBase.objects.first().id
        url = reverse('order:order_comments', kwargs={'id': id})
        data = {

        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(OrderComment.objects.count(), 19)


    # get lists of comments for a single order
    def test_get_single_order_comments(self):
        id = OrderBase.objects.first().id
        url = reverse('order:order_comments', kwargs={'id': id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ============================ order_files ==================================


    def test_create_order_files(self):
        id = OrderBase.objects.first().id

        file = open(settings.BASE_DIR + '/apps/order/fixtures/sample.pdf', 'rb')
        files = {'file': file}

        url = reverse('order:order_files', kwargs={'id':id})
        data = {
        'description': ' Sample description ',
        'kind': 'bill',
        'file': file
        }

        headers = {'Content-type': 'multipart/form-data'}
        response = self.client.post(url, files=files, data=data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderBase.objects.count(), 7)

    def test_create_order_files_missing_failed(self):
        id = OrderBase.objects.first().id


        url = reverse('order:order_files', kwargs={'id':id})
        data = {
        'description': ' Sample description ',
        'kind': 'bill',
        'file': None
        }

        headers = {'Content-type': 'multipart/form-data'}
        response = self.client.post(url, data=data, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(OrderBase.objects.count(), 7)

    # get lists of order files for a single order
    def test_get_all_order_files(self):
        id = OrderBase.objects.first().id
        url = reverse('order:order_files', kwargs={'id': id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # get lists of order files for a single order
    def test_get_order_files_for_none(self):
        id = 'a78ae3ee-cbd6-4cf5-83ba-3fe8dfa592b5' # not exists
        url = reverse('order:order_files', kwargs={'id': id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# ============================ single_order_file ==================================

    # get single file infomations
    def test_get_single_file(self):
        id = OrderFile.objects.first().id
        url = reverse('order:single_order_file', kwargs={'id':id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ============================ Order file tests ==================================

    def test_order_post(self):
        id = Account.objects.first().id
        url = reverse('order:order_port', kwargs={'id': id})
        data = {
            'kind': 'kind',
            'e164': '455',
            'port_type': 'port_type',
            'authorizer': 'authorizer',
            'address1': 'address1',
            'address2': 'address2',
            'city': 'city',
            'state': 'state',
            'zip': 'zip',
            'name': 'name',
            'btn': 'btn',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderBase.objects.count(), 8)

    def test_order_post_failed(self):
        id = Account.objects.first().id
        url = reverse('order:order_port', kwargs={'id': id})
        data = {
            'kind': 'kind',
            'e164': '',
            'port_type': 'port_type',
            'authorizer': 'authorizer',
            'address1': 'address1',
            'address2': 'address2',
            'city': 'city',
            'state': 'state',
            'zip': 'zip',
            'name': 'name',
            'btn': 'btn',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(OrderBase.objects.count(), 7)

    def test_order_post_failed1(self):
        id = Account.objects.first().id
        url = reverse('order:order_port', kwargs={'id': id})
        data = {
            'kind': 'kind',
            'e164': '455',
            'port_type': 'port_type',
            'authorizer': 'authorizer',
            'address1': 'address1',
            'address2': 'address2',
            'city': 'city',
            'state': 'state',
            'zip': 'zip',
            'name': 'name',
            'btn': '',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(OrderBase.objects.count(), 7)
