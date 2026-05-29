from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required, current_user
from app.models import Assessment, Response
from app import db
from app.questions import QUESTIONS
from datetime import datetime

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

    # Identify weaknesses
    weaknesses = []
    for r in responses:
        if r.answer == 'NO':
            q = next((x for x in QUESTIONS if x['id'] == r.question_id), None)
            if q:
                weaknesses.append(q)

    return render_template('assessment/results.html',
                           score=score_pct,
                           risk_level=risk_level,
                           weaknesses=weaknesses)