from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from server.models import Server, Route
import json


class ServerTests(APITestCase):
    fixtures = [
        'server_fixtures.json'
    ]

    # ============ 'accounts/<uuid:id>/routes'/routes ===========

    def test_create_route(self):
        url = reverse('server:routes', kwargs={"id": "0481db99-a303-4201-b6fe-b5560a3c8841"})  # account_id
        data = {
            "name": "sample route"
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Route.objects.count(), 7)

    def test_create_route_failed(self):
        url = reverse('server:routes', kwargs={'id': '0481db99-a303-4201-b6fe-b5560a3c8845'})  # single no. change
        data = {
            'name': 'create route_1'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Route.objects.count(), 6)

    def test_get_route_lists(self):
        self.test_create_route()
        url = reverse('server:routes', kwargs={"id": "0481db99-a303-4201-b6fe-b5560a3c8841"})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Route.objects.count(), 7)

    def test_get_route_lists_failed(self):
        self.test_create_route()
        url = reverse('server:routes', kwargs={"id": "0481db99-a303-4201-b6fe-b5560a3c8800"})  # 2 no. changed

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Route.objects.count(), 7)

    # ========= 'routes/<int:id>'/routes =========

    def test_get_single_route(self):
        id = Route.objects.first().id
        url = reverse('server:routes', kwargs={'id': id})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Route.objects.count(), 6)

    def test_single_route_failed(self):
        id = Route.objects.first().id + 1000000000000
        url = reverse('server:routes', kwargs={'id': id})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # patch route
    def test_update_route(self):
        id = Route.objects.first().id
        url = reverse('server:routes', kwargs={'id': id})
        data = {
            "name": "USA Gateway",
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Route.objects.count(), 6)

    # patch route failed
    def test_update_route_failed(self):
        id = Route.objects.first().id
        url = reverse('server:routes', kwargs={'id': id})
        data = {
            "name": "",
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Route.objects.count(), 6)

    # ============== 'servers'/route_servers ==============

    # server lists of data
    def test_get_lists(self):
        url = reverse('server:route_servers')
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Server.objects.count(), 8)

    # here new test for page test
    def test_get_lists_page_no(self):
        url = reverse('server:route_servers')
        data = {
            'page': 2
        }
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Server.objects.count(), 8)

        # ==================== route_servers ===================

    def test_route_server_lists(self):
        url = reverse('server:route_servers', kwargs={'id': 6})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Server.objects.count(), 8)

    def test_route_server_lists_not_found(self):
        url = reverse('server:route_servers', kwargs={'id': 60000})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Server.objects.count(), 8)

    def test_route_server_lists_page(self):
        url = reverse('server:route_servers', kwargs={'id': 6})
        data = {
            'page': 2
        }
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Server.objects.count(), 8)

    def test_route_server_create(self):
        id = Route.objects.first().id
        url = reverse('server:route_servers', kwargs={'id': id})
        data = {
            "uri": "sip:127.0.0.1:8002;transport=udp007",
            "weight": 54,
            "priority": 4916,
            "socket": "32.213.170.129",
            "state": 212,
            "attrs": "Sample attrs2",
            "algorithm": 24231,
            "name": "Test Server9050",
            "description": "Sample description",
            "kind": "Sample kind",
            "host": "127.0.0.1",
            "port": 8026,
            "transport": "udp",
            "channels": 1,
            "enabled": 1,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Server.objects.count(), 9)

    def test_route_server_create_failed(self):
        id = Route.objects.first().id
        url = reverse('server:route_servers', kwargs={'id': id})
        data = {
            "uri": "sip:127.0.0.1:8002;transport=udp",
            "weight": 54,
            "priority": 4916,
            "socket": "32.213.170.129",
            "state": 212,
            "attrs": "Sample attrs2",
            "algorithm": 24231,
            "name": "Test Server",
            "description": "Sample description",
            "kind": "Sample kind",
            "host": "127.0.0.1",
            "port": 8026,
            "transport": "udp",
            "channels": 1,
            "enabled": 1,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Server.objects.count(), 8)

    # ============================ single_server =============================

    # retrive single data
    def test_single_data(self):
        id = Server.objects.first().id
        url = reverse('server:single_server', kwargs={'id': id})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Server.objects.count(), 8)

    # not found single data
    def test_not_single_data(self):
        id = Server.objects.first().id + 10000000000
        url = reverse('server:single_server', kwargs={'id': id})
        data = {}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Server.objects.count(), 8)

    # patch server data
    def test_update_server(self):
        id = Server.objects.first().id
        url = reverse('server:single_server', kwargs={'id': id})
        data = {
            "state": 352,
            "attrs": "abcdfghijklmnopqrstuvwxyz",
            "algorithm": 45271,
            "name": "United_Xis",
            "description": "stringggggggggggg",
            "kind": "server_kind",
            "host": "127.0.0.2",
            "port": 8022,
            "transport": "udpx",
            "channels": 299,
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Server.objects.count(), 8)

    # patchin failed
    def test_update_server_failed(self):
        id = Server.objects.first().id
        url = reverse('server:single_server', kwargs={'id': id})
        data = {
            "state": 352,
            "attrs": '',
            "algorithm": 45271,
            "name": "United_Xis",
            "description": "stringggggggggggg",
            "kind": "server_kind",
            "host": "127.0.0.2",
            "port": 8022,
            "transport": "udpx",
            "channels": 299,
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Server.objects.count(), 8)


        # delete server data

    def test_delete_server(self):
        id = Server.objects.first().id
        url = reverse('server:single_server', kwargs={'id': id})
        data = {}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Server.objects.count(), 7)
