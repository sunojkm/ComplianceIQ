from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String(150), unique=True, nullable=False)
    password      = db.Column(db.String(150), nullable=False)
    company_name  = db.Column(db.String(150), nullable=False)
    industry      = db.Column(db.String(100), nullable=False)
    business_size = db.Column(db.String(50),  nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    assessments   = db.relationship('Assessment', backref='user', lazy=True)

class Assessment(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    started_at   = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    overall_score= db.Column(db.Float, nullable=True)
    risk_level   = db.Column(db.String(20), nullable=True)
    responses    = db.relationship('Response', backref='assessment', lazy=True)

class Response(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    question_id   = db.Column(db.Integer, nullable=False)
    answer        = db.Column(db.String(3), nullable=False)
    score         = db.Column(db.Integer, nullable=False)