from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Account


class AccountTests(APITestCase):



    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('account:accounts')
        data = {'name': 'Test Account 1'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'Test Account 1')

    def test_update_account(self):
        """
        Ensure we can update a new account object.
        """
        id = Account.objects.first().id
        url = reverse('account:accounts-detail', kwargs={"id":id})
        data = {'name': 'Updated Test Account 1'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'Updated Test Account 1')

    def test_delete_account(self):
        """
        Ensure we can delete a new account object.
        """
        id = Account.objects.first().id
        url = reverse('account:accounts-detail', kwargs={"id":id})
        data = {}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Account.objects.count(), 0)

