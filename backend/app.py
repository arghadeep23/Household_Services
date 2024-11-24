from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS
from models.User import User
from models.Admin import Admin
from models.Professional import Professional
from models.Service import Service
from models.ServiceRequest import ServiceRequest
from models.ServiceRemark import ServiceRemark
from models.base import Base
from routes.adminRoutes import admin_bp
from routes.userRoutes import user_bp
from routes.professionalRoutes import professional_bp
from routes.userAuthRoutes import auth_bp
from routes.professionalAuthRoutes import professional_auth_bp
from routes.ssoRoutes import sso_bp
from routes.serviceRoutes import service_bp
from routes.serviceRequestRoutes import service_request_bp

app = Flask(__name__)

# Enable CORS for all origins, headers, and methods
# Enable CORS for all origins, headers, and methods
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})


# Handle preflight requests explicitly
@app.after_request
@app.after_request 
def after_request(response): 
    response.headers["Access-Control-Allow-Origin"] = "*" 
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization" 
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS" 
    return response

# Database setup
engine = create_engine('sqlite:///householdServices.db')
Base.metadata.create_all(engine)

# Session setup
Session = sessionmaker(bind=engine)
session = Session()

# Register Blueprints
app.register_blueprint(admin_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(professional_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(professional_auth_bp, url_prefix='/api')
app.register_blueprint(sso_bp, url_prefix='/api')
app.register_blueprint(service_bp, url_prefix='/api')
app.register_blueprint(service_request_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
