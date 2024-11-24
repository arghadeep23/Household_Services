from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS # Import CORS
from models.User import User
from models.Admin import Admin
from models.Professional import Professional
from models.Service import Service
from models.ServiceRequest import ServiceRequest
from models.ServiceRemark import ServiceRemark
from models.base import Base  # Make sure to import Base from a common base module
from routes.adminRoutes import admin_bp
from routes.userRoutes import user_bp # For customers, mistakenly named as user, my bad
from routes.professionalRoutes import professional_bp
from routes.userAuthRoutes import auth_bp
from routes.professionalAuthRoutes import professional_auth_bp
from routes.ssoRoutes import sso_bp

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Database setup
engine = create_engine('sqlite:///householdServices.db')
Base.metadata.create_all(engine)

# Session setup
Session = sessionmaker(bind=engine)
session = Session()

# Register Blueprints (if you have any)
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(professional_bp, url_prefix='/api')
# customer signup and login
app.register_blueprint(auth_bp, url_prefix='/api')
# professional signup and login
app.register_blueprint(professional_auth_bp, url_prefix='/api')
# Single Sign-On
app.register_blueprint(sso_bp, url_prefix='/api')
# app.register_blueprint(your_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
