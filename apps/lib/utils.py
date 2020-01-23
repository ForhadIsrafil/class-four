from django.conf import settings
import requests
import smtplib
from email.mime.text import MIMEText
DATA_NO_PER_PAGE = 10

def slicer(data, page_i, limit=DATA_NO_PER_PAGE):
    limit = int(limit)
    start_idx = (page_i - 1) * limit
    end_idx = start_idx + limit
    return data[start_idx:end_idx]



def get_pagination(serialize_data, total_count, page): 
    response = {
        "data": serialize_data,
        "total_count": total_count,
        "page": page
    }
    return response


def update_user_session(uid):
    check_url = settings.OKTA_BASE_URL + '/api/v1/apps/' + settings.OKTA_CLIENT_ID + '/users/' + uid

    check_headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "SSWS " + settings.API_TOKEN
    }
    response = requests.get(check_url, headers=check_headers)

    if response.status_code == 200:
        return response
    else:
        return False


class Mailer():

    def send_email(self, subject,recipient, message):
        try:
            # START confirmation email

            sender = 'no-reply@telegents.com'
            message = message
            msg = MIMEText(message, 'html')
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = recipient

            server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(sender, [recipient], msg.as_string())
            server.quit()

            # END confirmation email
            return True
        except:
            return False