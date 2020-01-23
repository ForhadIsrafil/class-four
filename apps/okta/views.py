from django.shortcuts import render, redirect
# from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# import json
# import requests
# from django.conf import settings
# from django.db import transaction
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import status
# from django.conf import settings
#
#
# class CreateAccount(ViewSet):
#     @transaction.atomic
#     def create(self, request, format=None):
#         body = json.loads(request.body.decode('utf-8'))
#         print('body ', body)
#         firstname = body.get('firstname').strip()
#         lastname = body.get('lastname').strip()
#         email = body.get('email').strip()
#         password = body.get('password').strip()
#         if firstname is None or lastname is None or email is None or password is None:
#             return Response({'error': "'Field can't be empty!'"}, status=status.HTTP_400_BAD_REQUEST)
#
#         # password format ( at least one digit, capital letter )
#
#         url = settings.OKTA_BASE_URL + '/api/v1/users?activate=true'
#         data = {
#             "profile": {
#                 "firstName": firstname,
#                 "lastName": lastname,
#                 "email": email,
#                 "login": email
#             },
#             "credentials": {
#                 "password": {"value": password}
#             },
#             "groupIds": [
#                 settings.GROUP_ID
#             ]
#         }
#         headers = {
#             'Accept': 'application/json',
#             'Content-Type': 'application/json',
#             'Authorization': 'SSWS ' + settings.API_TOKEN
#         }
#         create_account = requests.post(url, data=json.dumps(data), headers=headers)
#         if create_account.status_code == 201:
#             print('create_account ', create_account.content)
#             return Response(create_account, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'error': 'Something Wrong!'},status=status.HTTP_400_BAD_REQUEST)
