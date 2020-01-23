import requests
from django.conf import settings
import json
def get_okta_user_info(uid):
    check_url = settings.OKTA_BASE_URL + '/api/v1/apps/' + settings.OKTA_CLIENT_ID + '/users/' + uid

    check_headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "SSWS " + settings.API_TOKEN
    }
    response = requests.get(check_url, headers=check_headers)

    if response.status_code == 200:
        return response.json()
    else:
        return False


def delete_account_and_role(id, arr):
    url = settings.OKTA_BASE_URL + '/api/v1/apps/' + settings.OKTA_CLIENT_ID + '/users/' + str(id)

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "SSWS " + settings.API_TOKEN
    }
    payload = {
        "profile": {
            "group_role": arr
        }
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response_data = response.json()
    return response_data.json()


def get_okta_user_profile_with_organization_info(uid):
    check_url = settings.OKTA_BASE_URL + '/api/v1/users/' + uid

    check_headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "SSWS " + settings.API_TOKEN
    }
    response = requests.get(check_url, headers=check_headers)

    if response.status_code == 200:
        return response.json()
    else:
        return False