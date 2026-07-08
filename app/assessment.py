from flask import Blueprint, render_template, request, redirect, url_for, session, make_response, flash
from flask_login import login_required, current_user
from app.models import Assessment, Response
from app import db
from app.questions import QUESTIONS
from datetime import datetime
from app.pdf_report import clean, generate_pdf

assessment = Blueprint('assessment', __name__)

@assessment.route('/assessment/start')
@login_required
def start():
    new_assessment = Assessment(user_id=current_user.id)
    db.session.add(new_assessment)
    db.session.commit()
    session['assessment_id'] = new_assessment.id
    session['question_index'] = 0
    return redirect(url_for('assessment.question'))

@assessment.route('/assessment/question', methods=['GET', 'POST'])
@login_required
def question():
    index = session.get('question_index', 0)
    assessment_id = session.get('assessment_id')

    if request.method == 'POST':
        answer = request.form.get('answer')
        q = QUESTIONS[index]
        score = q['weight'] if answer == 'YES' else 0

        response = Response(
            assessment_id=assessment_id,
            question_id=q['id'],
            answer=answer,
            score=score
        )
        db.session.add(response)
        db.session.commit()

        index += 1
        session['question_index'] = index

        if index >= len(QUESTIONS):
            return redirect(url_for('assessment.results'))

    if index >= len(QUESTIONS):
        return redirect(url_for('assessment.results'))

    q = QUESTIONS[index]
    progress = round((index / len(QUESTIONS)) * 100)
    return render_template('assessment/question.html',
                           question=q,
                           index=index,
                           total=len(QUESTIONS),
                           progress=progress)

@assessment.route('/assessment/results')
@login_required
def results():
    assessment_id = session.get('assessment_id')
    current_assessment = Assessment.query.get(assessment_id)
    responses = Response.query.filter_by(assessment_id=assessment_id).all()

    total_possible = sum(q['weight'] for q in QUESTIONS)
    total_scored   = sum(r.score for r in responses)
    score_pct      = round((total_scored / total_possible) * 100) if total_possible else 0

    themes = ['Organisational', 'People', 'Physical', 'Technological']
    theme_scores = {}
    for theme in themes:
        theme_qs       = [q for q in QUESTIONS if q['theme'] == theme]
        theme_possible = sum(q['weight'] for q in theme_qs)
        theme_ids      = [q['id'] for q in theme_qs]
        theme_scored   = sum(r.score for r in responses if r.question_id in theme_ids)
        theme_scores[theme] = round((theme_scored / theme_possible) * 100) if theme_possible else 0

    if score_pct >= 80:
        risk_level = 'Low'
    elif score_pct >= 60:
        risk_level = 'Medium'
    elif score_pct >= 40:
        risk_level = 'High'
    else:
        risk_level = 'Critical'

    current_assessment.overall_score = score_pct
    current_assessment.risk_level    = risk_level
    current_assessment.completed_at  = datetime.utcnow()
    db.session.commit()

    weaknesses = []
    for r in responses:
        if r.answer == 'NO':
            q = next((x for x in QUESTIONS if x['id'] == r.question_id), None)
            if q:
                weaknesses.append(q)

    return render_template('results/results.html',
                           score=score_pct,
                           risk_level=risk_level,
                           weaknesses=weaknesses,
                           theme_scores=theme_scores)


@assessment.route('/assessment/results/<int:assessment_id>')
@login_required
def view_results(assessment_id):
    current_assessment = Assessment.query.get_or_404(assessment_id)

    if current_assessment.user_id != current_user.id:
        return redirect(url_for('main.dashboard'))

    responses = Response.query.filter_by(assessment_id=assessment_id).all()

    themes = ['Organisational', 'People', 'Physical', 'Technological']
    theme_scores = {}
    for theme in themes:
        theme_qs       = [q for q in QUESTIONS if q['theme'] == theme]
        theme_possible = sum(q['weight'] for q in theme_qs)
        theme_ids      = [q['id'] for q in theme_qs]
        theme_scored   = sum(r.score for r in responses if r.question_id in theme_ids)
        theme_scores[theme] = round((theme_scored / theme_possible) * 100) if theme_possible else 0

    weaknesses = []
    for r in responses:
        if r.answer == 'NO':
            q = next((x for x in QUESTIONS if x['id'] == r.question_id), None)
            if q:
                weaknesses.append(q)

    session['assessment_id'] = assessment_id

    return render_template('results/results.html',
                           score=current_assessment.overall_score,
                           risk_level=current_assessment.risk_level,
                           weaknesses=weaknesses,
                           theme_scores=theme_scores)


@assessment.route('/assessment/download-pdf')
@login_required
def download_pdf():
    assessment_id = session.get('assessment_id')
    if not assessment_id:
        return redirect(url_for('main.dashboard'))

    current_assessment = Assessment.query.get(assessment_id)
    responses = Response.query.filter_by(assessment_id=assessment_id).all()

    themes = ['Organisational', 'People', 'Physical', 'Technological']
    theme_scores = {}
    for theme in themes:
        theme_qs       = [q for q in QUESTIONS if q['theme'] == theme]
        theme_possible = sum(q['weight'] for q in theme_qs)
        theme_ids      = [q['id'] for q in theme_qs]
        theme_scored   = sum(r.score for r in responses if r.question_id in theme_ids)
        theme_scores[theme] = round((theme_scored / theme_possible) * 100) if theme_possible else 0

    weaknesses = []
    for r in responses:
        if r.answer == 'NO':
            q = next((x for x in QUESTIONS if x['id'] == r.question_id), None)
            if q:
                weaknesses.append(q)

    pdf_bytes = generate_pdf(
        company_name  = clean(current_user.company_name),
        industry      = clean(current_user.industry),
        business_size = clean(current_user.business_size),
        score         = current_assessment.overall_score,
        risk_level    = current_assessment.risk_level,
        theme_scores  = theme_scores,
        weaknesses    = weaknesses
    )

    response = make_response(pdf_bytes)
    response.headers['Content-Type']        = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=ComplianceIQ_Report_{current_user.company_name}.pdf'
    return response

@assessment.route('/assessment/delete/<int:assessment_id>', methods=['POST'])
@login_required
def delete_assessment(assessment_id):
    current_assessment = Assessment.query.get_or_404(assessment_id)

    # Security check — users can only delete their own assessments
    if current_assessment.user_id != current_user.id:
        flash('Unauthorised action.', 'error')
        return redirect(url_for('main.dashboard'))

    # Delete responses first then assessment
    Response.query.filter_by(assessment_id=assessment_id).delete()
    db.session.delete(current_assessment)
    db.session.commit()

    flash('Assessment deleted successfully.', 'success')
    return redirect(url_for('main.dashboard'))