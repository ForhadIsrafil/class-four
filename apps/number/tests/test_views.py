from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from account.models import Account, AccountNumber
from number.models import Number
import json
from django.test.client import encode_multipart, RequestFactory


class NumberTests(APITestCase):
    fixtures = [
        'number_fixtures.json',
    ]

    # ====================== numbers ======================

    def test_get_number_lists(self):
        url = reverse('number:numbers')
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_number(self):
        url = reverse('number:numbers', )
        data = {
            'e164': '54647978',
            'status': 'portedin'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Number.objects.count(), 10)

    def test_post_number_failed(self):
        url = reverse('number:numbers', )
        data = {
            'e164': '7135551215',
            'status': 'portedin'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'e164 already exists')
        self.assertEqual(Number.objects.count(), 9)

    def test_post_number_failed1(self):
        url = reverse('number:numbers', )
        data = {
            'e164': "",
            'status': 'portedin'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'e164 field required')
        self.assertEqual(Number.objects.count(), 9)

    # ====================== single_number ======================

    def test_retrieve_number(self):
        e164 = Number.objects.first().e164
        url = reverse('number:single_number', kwargs={'e164_id': e164})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_number_failed(self):
        e164 = Number.objects.first().e164 + '10000000000000'
        url = reverse('number:single_number', kwargs={'e164_id': e164})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_number(self):
        url = reverse('number:single_number', kwargs={'e164_id': 7135551215})
        data = {
            'e164': '7135551215',
            'status': 'portedout'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Number.objects.count(), 9)

    def test_update_number_failed(self):
        url = reverse('number:single_number', kwargs={'e164_id': 7135551215})
        data = {
            'e164': '7135551215',
            'status': 'xyzt'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Number.objects.count(), 9)

    # ========================= account_numbers ===========================

    def test_accountnumbers_lists(self):
        id = Account.objects.first().id
        url = reverse('number:account_numbers', kwargs={'id': id})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ===================Account Number Create ==========================
    #
    def test_post_accountnumber(self):
        id = Account.objects.first().id
        url = reverse('number:account_numbers', kwargs={'id': id})
        data = {
        'number': 'http://127.0.0.1:8000/api/v1/numbers/7135551211'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # ============================= single_account_number =======================

    def test_single_account_number(self):
        id = AccountNumber.objects.first().id
        url = reverse('number:single_account_number', kwargs={'id': id})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ============================= account_number_lidb ===========================

    def test_lidb_lists(self):
        id = AccountNumber.objects.first().id
        url = reverse('number:account_number_lidb', kwargs={'id': id})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lidb_request_methode_failed(self):
        id = AccountNumber.objects.first().id
        url = reverse('number:account_number_lidb', kwargs={'id': id})
        data = {
            'name': 'Sample Lidb name',
            'kind': 'business'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_lidb_lists_not_found(self):
        id = '57545bc8-c41a-41b0-a255-51833289620c'
        url = reverse('number:account_number_lidb', kwargs={'id': id})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_lidb(self):
        id = AccountNumber.objects.first().id
        url = reverse('number:account_number_lidb', kwargs={'id': id})
        data = {
            'name': 'Sample Lidb name',
            'kind': 'business'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #  =========================== account_e911 =========================

    # Account_E911 lists
    def test_e911_lists(self):
        id = AccountNumber.objects.first().id
        url = reverse('number:account_e911', kwargs={'id': id})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Account_E911 put
    def test_e911_update(self):
        id = AccountNumber.objects.first().id
        url = reverse('number:account_e911', kwargs={'id': id})
        data = {
            'address1': 'string',
            'address2': 'string',
            'city': 'string',
            'state': 'ua',
            'zipcode': '1206',
            'zipcode2': '1204',
            'comment': 'hahaha'
        }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
