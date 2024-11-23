from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.User import User
from models.Admin import Admin
from models.Professional import Professional
from models.Service import Service
from models.ServiceRequest import ServiceRequest
from models.ServiceRemark import ServiceRemark
from models.base import Base  # Make sure to import Base from a common base module
from routes.adminRoutes import admin_bp

app = Flask(__name__)

# Database setup
engine = create_engine('sqlite:///householdServices.db')
Base.metadata.create_all(engine)

# Session setup
Session = sessionmaker(bind=engine)
session = Session()

# Register Blueprints (if you have any)
app.register_blueprint(admin_bp, url_prefix='/api')
# app.register_blueprint(your_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
