from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.models import Account


class AccountTests(APITestCase):
    # import fixtures
    fixtures = ['initial_fixtures.json']

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('account:accounts')
        data = {'name': 'Test Account 1',"description": "descriptions here"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 24)

    def test_unique_name_test(self):
        self.test_create_account()
        """
        Ensure we can create a new account object.
        """
        url = reverse('account:accounts')
        data = {'name': 'Test Account 1',"description": "descriptions here2"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Account.objects.count(), 24)

    # failed if requires field is empty
    def test_required_field_error(self):
        url = reverse('account:accounts')
        data = {'name': None}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_fail_account(self):
        url = reverse('account:accounts')
        data = {'description': 'description100'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # get lists of data of accounts

    def test_get_lists(self):
        url = reverse('account:accounts', )
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_account(self):
        """
        Ensure we can update a new account object.
        """
        id = Account.objects.first().id
        url = reverse('account:accounts-detail', kwargs={"id": id})
        data = {'name': 'Updated string'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Account.objects.count(), 23)

    def test_delete_account(self):
        """
        Ensure we can delete a new account object.
        """
        id = Account.objects.first().id
        url = reverse('account:accounts-detail', kwargs={"id": id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Account.objects.count(), 22)



    # get single user data
    def test_single_retrive(self):
        id = Account.objects.first().id
        url = reverse('account:accounts-detail', kwargs={'id': id})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Account.objects.count(), 23)

    def test_get_lists_page_no(self):
        url = reverse('account:accounts')
        data = {
            'page': 2
        }
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
