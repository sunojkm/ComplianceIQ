from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import Assessment
from app import db

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def dashboard():
    assessments = Assessment.query.filter_by(
        user_id=current_user.id
    ).order_by(Assessment.completed_at.desc()).limit(5).all()
    return render_template('main/dashboard.html',
                           user=current_user,
                           assessments=assessments)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        action = request.form.get('action')

        # Update company details
        if action == 'update_details':
            current_user.company_name  = request.form.get('company_name')
            current_user.industry      = request.form.get('industry')
            current_user.business_size = request.form.get('business_size')
            db.session.commit()
            flash('Company details updated successfully.', 'success')
            return redirect(url_for('main.profile'))

        # Change password
        if action == 'change_password':
            current_password = request.form.get('current_password')
            new_password     = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            if not check_password_hash(current_user.password, current_password):
                flash('Current password is incorrect.', 'error')
                return redirect(url_for('main.profile'))

            if new_password != confirm_password:
                flash('New passwords do not match.', 'error')
                return redirect(url_for('main.profile'))

            if len(new_password) < 6:
                flash('New password must be at least 6 characters.', 'error')
                return redirect(url_for('main.profile'))

            current_user.password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password changed successfully.', 'success')
            return redirect(url_for('main.profile'))

    total_assessments = Assessment.query.filter_by(
        user_id=current_user.id
    ).filter(Assessment.completed_at != None).count()

    return render_template('main/profile.html',
                           user=current_user,
                           total_assessments=total_assessments)