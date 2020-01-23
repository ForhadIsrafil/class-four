from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status
from account.models import AccountNumber, Account, AccountServer, E911
from account.serializers import AccountSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import parsers, renderers, status
import json
from django.db import transaction
from account.utils import slicer
from django.shortcuts import get_object_or_404
from apps.lib.views import ViewSet
from apps.lib.utils import get_pagination, Mailer
from django.conf import settings
import requests
from okta.models import OktaUserInfo
from account.service import get_okta_user_info, get_okta_user_profile_with_organization_info
from rest_framework import viewsets


class OktaSignup(ViewSet):
    @transaction.atomic
    def create(self, request, format=None):
        body = json.loads(request.body.decode('utf-8'))
        firstname = body.get('firstname').strip()
        lastname = body.get('lastname').strip()
        email = body.get('email')
        password = body.get('password').strip()
        # family_name = body.get('family_name')

        if firstname == '' or lastname == '' or email == '' or password == '':
            return Response({'error': 'Field can\'t be empty. All fields are required!'},
                            status=status.HTTP_400_BAD_REQUEST)

        # checking family name avaibality end

        url = settings.OKTA_BASE_URL + "/api/v1/users?activate=false"
        data = {
            "profile": {
                "firstName": firstname,
                "lastName": lastname,
                "email": email,
                "login": email
                # "organization": family_name
            },
            "credentials": {
                "password": {"value": password},
                "recovery_question": {
                    "question": "Who's a major player in the cowboy scene?",
                    "answer": "Annie Oakley"
                }
            },
            "groupIds": [
                settings.GROUP_ID
            ]
        }
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/json",
            "Authorization": "SSWS " + settings.API_TOKEN,
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5"
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        json_response = json.loads(response.content.decode('utf-8'))

        if response.status_code != 200:
            return Response(json.loads(response.content.decode('utf-8')), status=status.HTTP_400_BAD_REQUEST)

        mailer = Mailer()
        email_body = '<strong> Welcome to Telegents Family! </strong> <p>You’ve joined Telegents Family successfully. Please click given link below to activate ' \
                     'your account.</p><p> Thank you </p>'

        email_body += settings.FRONTEND_URL + '/active-account?user=' + json_response['id']

        subject = 'Telegents: Registration'

        email_response = mailer.send_email(subject=subject, recipient=json_response['profile']['email'],
                                           message=email_body)
        if email_response is False:
            return Response({"error": "Email sending process failed."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if response.status_code == 200:
            return Response(
                {'success': 'Your account is successfully created!.Please check your email to activate your account.'},
                status=status.HTTP_201_CREATED)
        else:
            return Response(json.loads(response.content.decode('utf-8')),
                            status=status.HTTP_400_BAD_REQUEST)


class OktaSignin(ViewSet):

    @transaction.atomic
    def create(self, request, format=None):
        body = json.loads(request.body.decode('utf-8'))
        username = body.get('email').strip()
        password = body.get('password').strip()
        if username == '' or password == '':
            return Response({'error': "Field can't be empty.All fields are required!"},
                            status=status.HTTP_400_BAD_REQUEST)

        url = settings.OKTA_BASE_URL + "/api/v1/authn"
        data = {
            "password": password,
            "username": username
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "SSWS " + settings.API_TOKEN,
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            response_data = json.loads(response.content.decode('utf-8'))
            session_token = response_data['sessionToken']

            okta_user_id = response_data['_embedded']['user']['id']

            session_url = settings.OKTA_BASE_URL + "/api/v1/sessions/"
            data = {
                "sessionToken": session_token
            }
            session_response = requests.post(session_url, data=json.dumps(data), headers=headers)

            session_response_data = json.loads(session_response.content.decode('utf-8'))
            response_data['sessionToken'] = session_response_data['id']

            # collecting account infos
            okta_user_info = get_okta_user_info(okta_user_id)

            if not okta_user_info:
                return Response({'error': 'We Could not found your group role information. Something must wrong .'},
                                status=status.HTTP_400_BAD_REQUEST)

            arr = []
            previous_group_roles = okta_user_info['profile']['group_role']

            if previous_group_roles is not None or previous_group_roles == []:
                for role in previous_group_roles:
                    arr.append(role)

            response_data['account_info'] = arr

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(json.loads(response.content.decode('utf-8')),
                            status=status.HTTP_400_BAD_REQUEST)


class OktaLogout(ViewSet):

    def destroy(self, request):
        session_token = request.META.get('HTTP_AUTHORIZATION').strip()
        type, token = session_token.split()

        okta_info = OktaUserInfo.objects.filter(session_id=token).first()

        if okta_info is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        create_session_url = settings.OKTA_BASE_URL + "/api/v1/sessions/" + okta_info.session_id
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "SSWS " + settings.API_TOKEN
        }

        delete_session = requests.delete(create_session_url, data={},
                                         headers=headers)  # Closes a user’s session (logout).(for web)

        okta_info.access_token = None
        okta_info.session_id = None
        okta_info.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivateUserAccount(ViewSet):
    @transaction.atomic
    def create(self, request, userid, format=None):
        activate_url = settings.OKTA_BASE_URL + '/api/v1/users/' + userid + '/lifecycle/activate?sendEmail=false'
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "SSWS " + settings.API_TOKEN
        }
        activate_response = requests.post(activate_url, data={}, headers=headers)
        if activate_response.status_code == 200:
            return Response({'success': 'Your account is successfully activated!.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(json.loads(activate_response.content.decode('utf-8')), status=status.HTTP_400_BAD_REQUEST)


class ForgetPassword(ViewSet):
    def create(self, request):
        body = json.loads(request.body.decode('utf-8'))

        username = body.get('email')
        if username == '' or username == None:
            return Response({'error': "'Field can't be empty.Email is required!'"},
                            status=status.HTTP_400_BAD_REQUEST)

        recovery_url = settings.OKTA_BASE_URL + "/api/v1/authn/recovery/password"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "SSWS " + settings.API_TOKEN,
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
            "X-Forwarded-For": "23.235.46.133"
        }

        data = {
            "username": username
        }

        recovery_response = requests.post(recovery_url, data=json.dumps(data),
                                          headers=headers)

        if recovery_response.status_code != 200:
            return Response(json.loads(recovery_response.content.decode('utf-8')), status=status.HTTP_400_BAD_REQUEST)

        recovery_response_data = json.loads(recovery_response.content.decode('utf-8'))

        recoveryToken = recovery_response_data['recoveryToken']

        mailer = Mailer()
        email_body = '<strong> Hello Telegent\'s Member! </strong> <p>You’ve requested to reset your password. Please click given link below to reset your password' \
                     '.</p><p> Thank you </p>'

        email_body += settings.FRONTEND_URL + '/reset-password?recovery_token=' + recoveryToken

        subject = 'Telegents: Forget Password'

        email_response = mailer.send_email(subject=subject, recipient=username, message=email_body)

        if email_response is False:
            return Response({"error": "Email sending process failed."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {'success': 'Please check your email to reset your password.'},
            status=status.HTTP_200_OK)


class ResetPassword(ViewSet):

    def create(self, request):
        body = json.loads(request.body.decode('utf-8'))

        recoveryToken = body.get('recovery_token')
        newPassword = body.get('new_password')
        if recoveryToken == '' or newPassword == '':
            return Response({'error': "'Field can't be empty.All fields are required!'"},
                            status=status.HTTP_400_BAD_REQUEST)

        recovery_token_url = settings.OKTA_BASE_URL + "/api/v1/authn/recovery/token"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        data = {
            "recoveryToken": recoveryToken
        }

        recovery_token_response = requests.post(recovery_token_url, data=json.dumps(data),
                                                headers=headers)

        if recovery_token_response.status_code != 200:
            return Response(json.loads(recovery_token_response.content.decode('utf-8')),
                            status=status.HTTP_400_BAD_REQUEST)

        recovery_token_response_data = json.loads(recovery_token_response.content.decode('utf-8'))

        stateToken = recovery_token_response_data['stateToken']

        question_answer_url = settings.OKTA_BASE_URL + "/api/v1/authn/recovery/answer"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "SSWS " + settings.API_TOKEN
        }

        data = {
            "stateToken": stateToken,
            "answer": "Annie Oakley"
        }

        question_answer_response = requests.post(question_answer_url, data=json.dumps(data),
                                                 headers=headers)

        if question_answer_response.status_code != 200:
            return Response(json.loads(question_answer_response.content.decode('utf-8')),
                            status=status.HTTP_400_BAD_REQUEST)

        question_answer_response_data = json.loads(question_answer_response.content.decode('utf-8'))

        FinalStateToken = question_answer_response_data['stateToken']

        reset_password_url = settings.OKTA_BASE_URL + "/api/v1/authn/credentials/reset_password"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "SSWS " + settings.API_TOKEN
        }

        data = {
            "stateToken": FinalStateToken,
            "newPassword": newPassword
        }
        reset_password_response = requests.post(reset_password_url, data=json.dumps(data),
                                                headers=headers)
        if reset_password_response.status_code != 200:
            return Response(json.loads(reset_password_response.content.decode('utf-8')),
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Password successfully reset.Please login again'},
                        status=status.HTTP_200_OK)
