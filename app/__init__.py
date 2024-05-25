# Initializes configurations.
# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
import yaml

app = Flask(__name__)

# Load configuration from YAML file
with open('C:\\Users\\blake\\Documents\\github\\musichost_creds.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

app.config['SECRET_KEY'] = config.get('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///C://Users//blake//Documents//github//musichost_site.db')

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app)

from app import routes

