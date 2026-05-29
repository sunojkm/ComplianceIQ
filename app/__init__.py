from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'complianceiq-secret-2025'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///complianceiq.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.auth import auth as auth_blueprint
    from app.main import main as main_blueprint
    from app.assessment import assessment as assessment_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(assessment_blueprint)

    with app.app_context():
        db.create_all()

    return app