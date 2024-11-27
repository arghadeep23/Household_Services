import requests
import resend
from celery.schedules import crontab
from celeryconfig import make_celery
from app import app

# Initialize Celery
celery = make_celery(app)

# Set up Resend API key
resend.api_key = "re_bHhjLKFb_22nxEWAmuotHuND85Db1VCsn"


@celery.task
def send_email(to, subject, body):
    params = {
        "from": "Acme <onboarding@resend.dev>",
        "to": [to],
        "subject": subject,
        "html": body,
    }

    r = resend.Emails.send(params)
    return r


@celery.task
def check_and_send_reminders():
    professionals = get_professionals()
    for professional_id in professionals:
        url = f'http://localhost:5000/api/service_requests/professional/{professional_id}'
        response = requests.get(url)
        service_requests = response.json()

        for request in service_requests:
            if request['status'] == 'Accepted':
                email_body = f"<strong>You have a pending service request with ID: {request['id']}</strong>"
                send_email.delay(
                    request['professional_id'], 'Pending Service Request Reminder', email_body)


def get_professionals():
    return [4]  # Example IDs


celery.conf.beat_schedule = {
    'send-reminders-every-5-minutes': {
        'task': 'tasks.check_and_send_reminders',
        'schedule': crontab(minute='*/5'),
    }
}
