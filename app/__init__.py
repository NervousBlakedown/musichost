from flask import Flask
from .extensions import db, login_manager, csrf
import yaml

def create_app():
    app = Flask(__name__)

    # Load configuration from YAML file
    with open('C:\\Users\\blake\\Documents\\github\\musichost_creds.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    app.config['SECRET_KEY'] = config.get('SECRET_KEY', 'default_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///C://Users//blake//Documents//github//musichost_site.db')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Set the login view
    login_manager.login_view = 'main.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
