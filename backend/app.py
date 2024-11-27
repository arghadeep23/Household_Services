from routes.serviceRemarkRoutes import service_remark_bp
from routes.serviceRequestRoutes import service_request_bp
from routes.serviceRoutes import service_bp
from routes.ssoRoutes import sso_bp
from routes.professionalAuthRoutes import professional_auth_bp
from routes.userAuthRoutes import auth_bp
from routes.professionalRoutes import professional_bp
from routes.userRoutes import user_bp
from routes.adminRoutes import admin_bp
from flask import Flask
from sqlalchemy import create_engine
from celeryconfig import make_celery
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_cors import CORS
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os
from flask_mail import Mail, Message
from celery import schedules
import requests

load_dotenv()
print(os.getenv("MAIL_SERVER"))
print(os.getenv("MAIL_PORT"))
print(os.getenv("MAIL_USERNAME"))
print(os.getenv("MAIL_PASSWORD"))


def create_app():
    # Load environment variables

    # Flask App Initialization
    app = Flask(__name__)

    # JWT Configuration
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    jwt = JWTManager(app)

    # Celery configuration
    app.config.update(
        broker_url='redis://localhost:6379/0',     # Updated key
        result_backend='redis://localhost:6379/0'  # Updated key
    )

    # Initialize Celery using make_celery function
    celery_app = make_celery(app)
    celery_app.conf.beat_schedule = {
        'send-reminders-every-5-minutes': {
            'task': 'tasks.check_and_send_reminders',
            'schedule': schedules.crontab(minute='*/5'),
        }
    }

    # Enable CORS
    CORS(app)

    # Mail setup
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER", "smtp.example.com")
    app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv(
        "MAIL_DEFAULT_SENDER", "noreply@example.com")

    mail = Mail(app)

    # Database setup
    Base = declarative_base()
    engine = create_engine('sqlite:///householdServices.db')
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    # Register blueprints
    app.register_blueprint(admin_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(professional_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(professional_auth_bp, url_prefix='/api')
    app.register_blueprint(sso_bp, url_prefix='/api')
    app.register_blueprint(service_bp, url_prefix='/api')
    app.register_blueprint(service_request_bp, url_prefix='/api')
    app.register_blueprint(service_remark_bp, url_prefix='/api')

    @app.route("/")
    def index():
        return "Hello, World!"

    return app, celery_app


app, _ = create_app()
celery_app = make_celery(app)
celery_app.conf.beat_schedule = {
    'send-reminders-every-5-minutes': {
        'task': 'tasks.check_and_send_reminders',
        'schedule': schedules.crontab(minute='*/1'),
    }
}

# Mail setup
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER", "smtp.example.com")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 465))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = os.getenv(
    "MAIL_DEFAULT_SENDER", "noreply@example.com")


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
                mail = Mail(app)
                try:

                    mail.send(msg)
                except Exception as e:
                    print("Error sending mail")
                    print(e)


def get_professional_email(professional_id):
    # Replace with actual logic to fetch professional email
    # Example API call or database query
    response = requests.get(
        f"http://localhost:5000/api/professionals/{professional_id}")
    # return response.json().get('email')
    return "deyarghadeep23@gmail.com"


if __name__ == '__main__':
    app, _ = create_app()
    app.run(debug=True)

# celery -A app.celery_app beat --loglevel=info
# celery - A app.celery_app worker - -loglevel = info
# source .venv/bin/activate
