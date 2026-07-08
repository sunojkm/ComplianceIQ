from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db, limiter

auth = Blueprint('auth', __name__)

@auth.route('/landing')
def landing():
    from flask_login import current_user
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('auth/landing.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email         = request.form.get('email')
        password      = request.form.get('password')
        company_name  = request.form.get('company_name')
        industry      = request.form.get('industry')
        business_size = request.form.get('business_size')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered.', 'error')
            return redirect(url_for('auth.register'))

        new_user = User(
            email         = email,
            password      = generate_password_hash(password),
            company_name  = company_name,
            industry      = industry,
            business_size = business_size
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please sign in to continue.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        email    = request.form.get('email')
        password = request.form.get('password')
        user     = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid credentials. Please check your email and password.', 'error')
            return redirect(url_for('auth.login'))

        login_user(user)
        return redirect(url_for('main.dashboard'))

    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.landing'))


@auth.route('/forgot-password')
def forgot_password():
    return render_template('auth/forgot_password.html')