from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

db = SQLAlchemy()
login_manager = LoginManager()
limiter = Limiter(get_remote_address, default_limits=["200 per day", "50 per hour"])
# limiter = Limiter(get_remote_address, default_limits=[])

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'complianceiq-secret-2025')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///complianceiq.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['RATELIMIT_STORAGE_URI'] = 'memory://'

    db.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    login_manager.login_view = 'auth.landing'
    # login_manager.login_view = 'auth.login'

    from app.auth import auth as auth_blueprint
    from app.main import main as main_blueprint
    from app.assessment import assessment as assessment_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(assessment_blueprint)

    with app.app_context():
        db.create_all()

    return app