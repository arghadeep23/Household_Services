import requests
from worker import celery_app
from flask_mail import Message
from flask import current_app as app
from app import mail


@celery_app.task(name="tasks.check_and_send_reminders")
def check_and_send_reminders():
    with app.app_context():
        # Assuming you have a list of professional IDs to loop through
        # Update this logic to dynamically fetch IDs if needed
        professional_ids = [4]

        for professional_id in professional_ids:
            response = requests.get(
                f"http://localhost:5000/api/service_requests/professional/{professional_id}")
            service_requests = response.json()  # Array of service request objects

            accepted_requests = [
                req for req in service_requests if req['status'] == 'Accepted'
            ]

            if accepted_requests:
                # Prepare email body with accepted requests details
                services_details = "\n".join(
                    [f"- {req['selected_subservices'][0]['name']} (₹{req['selected_subservices'][0]['basePrice']})"
                     for req in accepted_requests]
                )

                # Fetch professional email dynamically (assuming it's part of the response, or fetch separately)
                professional_email = get_professional_email(
                    professional_id)  # Implement this function to fetch email

                msg = Message(
                    subject="Reminder: Pending Work",
                    recipients=[professional_email],
                    body=f"Hello Professional {professional_id},\n\nYou have the following accepted service requests:\n\n{services_details}\n\nPlease ensure timely action."
                )
                mail.send(msg)


def get_professional_email(professional_id):
    # Replace with actual logic to fetch professional email
    # Example API call or database query
    response = requests.get(
        f"http://localhost:5000/api/professionals/{professional_id}")
    return response.json().get('email')
