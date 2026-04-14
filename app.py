import os
import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from models import db, User, Question, Attempt

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'gre-quant-dev-secret-2024')

db_url = os.environ.get('DATABASE_URL', 'sqlite:///gre_quant.db')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    from data.seed import seed_if_empty
    seed_if_empty()


# ---------------------------------------------------------------------------
# Question selection
# ---------------------------------------------------------------------------

def select_question(user):
    """Select the next question for the user based on their level and history."""
    recent_attempts = (
        Attempt.query.filter_by(user_id=user.id)
        .order_by(Attempt.created_at.desc())
        .limit(20)
        .all()
    )
    recent_ids = {a.question_id for a in recent_attempts}

    content_levels = user.content_levels
    weak_area = min(content_levels, key=lambda k: content_levels[k])
    level = int(user.thinking_level)

    # Try weak area, at or below current thinking level
    q = (
        Question.query.filter(
            Question.content_area == weak_area,
            Question.thinking_level <= level,
            ~Question.id.in_(recent_ids),
        )
        .first()
    )

    if not q:
        # Any unanswered/not-recent question
        q = (
            Question.query.filter(
                Question.thinking_level <= level,
                ~Question.id.in_(recent_ids),
            )
            .first()
        )

    if not q:
        # Reset — pick any question randomly
        q = (
            Question.query.filter(Question.thinking_level <= max(1, level))
            .order_by(db.func.random())
            .first()
        )

    return q


# ---------------------------------------------------------------------------
# Answer checking
# ---------------------------------------------------------------------------

def check_answer(question, user_answer):
    """Return True if user_answer matches the correct answer."""
    correct = question.correct_answer

    if question.question_type == 'MA':
        if isinstance(user_answer, list) and isinstance(correct, list):
            return sorted(str(a).strip() for a in user_answer) == sorted(
                str(c).strip() for c in correct
            )
        return False

    if question.question_type == 'NE':
        try:
            return abs(float(str(user_answer).strip()) - float(str(correct))) < 0.01
        except (ValueError, TypeError):
            return False

    # QC / MC — single string
    return str(user_answer).strip() == str(correct).strip()


# ---------------------------------------------------------------------------
# Feedback generation
# ---------------------------------------------------------------------------

def generate_feedback(question, user_answer, is_correct):
    """Return coach feedback (AI if key present, else stored data)."""
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if api_key:
        return _ai_feedback(question, user_answer, is_correct, api_key)
    return _stored_feedback(question, user_answer, is_correct)


def _stored_feedback(question, user_answer, is_correct):
    lines = []

    if is_correct:
        lines.append("**إجابة صحيحة! ✓**")
        if question.concept_explanation:
            lines.append(f"\n**المفهوم الأساسي:** {question.concept_explanation}")
        if question.decision_explanation:
            lines.append(f"\n**قاعدة القرار:** {question.decision_explanation}")
        traps = question.trap_tags
        if traps:
            lines.append(f"\n**تنبيه — راقب الفخ:** {', '.join(traps)}")
    else:
        lines.append(
            f"**إجابة خاطئة. ✗**  إجابتك: *{user_answer}* | الصحيح: *{question.correct_answer}*"
        )
        steps = question.solution_steps
        if steps:
            lines.append("\n**خطوات الحل:**")
            for i, step in enumerate(steps, 1):
                lines.append(f"{i}. {step}")
        if question.concept_explanation:
            lines.append(f"\n**المفهوم:** {question.concept_explanation}")
        mistakes = question.common_mistakes
        if mistakes:
            lines.append("\n**الأخطاء الشائعة:**")
            for m in mistakes:
                lines.append(f"• {m}")
        if question.decision_explanation:
            lines.append(f"\n**قاعدة القرار:** {question.decision_explanation}")

    return "\n".join(lines)


def _ai_feedback(question, user_answer, is_correct, api_key):
    try:
        import anthropic

        with open('SYSTEM_PROMPT.txt', 'r', encoding='utf-8') as f:
            system_prompt = f.read()

        q_parts = [f"**السؤال:** {question.stem_ar}"]
        if question.question_type == 'QC':
            if question.condition_ar:
                q_parts.append(f"الشرط: {question.condition_ar}")
            q_parts.append(f"العمود (أ): {question.col_a_ar}")
            q_parts.append(f"العمود (ب): {question.col_b_ar}")
        elif question.choices:
            q_parts.append(f"الخيارات: {', '.join(question.choices)}")

        q_text = "\n".join(q_parts)
        msg = (
            f"{q_text}\n\n"
            f"**إجابة الطالب:** {user_answer}\n"
            f"**الإجابة الصحيحة:** {question.correct_answer}\n"
            f"**النتيجة:** {'صحيحة ✓' if is_correct else 'خاطئة ✗'}\n\n"
            "قدم تعليقاً مختصراً وتدريبياً كمدرب GRE. "
            "إذا كانت الإجابة خاطئة، حدد نوع الخطأ واشرح لماذا."
        )

        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            system=system_prompt,
            messages=[{"role": "user", "content": msg}],
        )
        return response.content[0].text
    except Exception:
        return _stored_feedback(question, user_answer, is_correct)


# ---------------------------------------------------------------------------
# Stats update
# ---------------------------------------------------------------------------

def update_user_stats(user, question, is_correct):
    """Adjust content level scores and thinking level after an attempt."""
    area = question.content_area
    levels = user.content_levels

    if is_correct:
        levels[area] = min(5.0, levels.get(area, 3.0) + 0.5)
    else:
        levels[area] = max(1.0, levels.get(area, 3.0) - 0.3)

    levels[area] = round(levels[area], 1)
    user.content_levels = levels

    # Recalculate thinking level from average content level
    avg = sum(levels.values()) / len(levels)
    user.thinking_level = min(4, max(1, round(avg / 1.25)))

    db.session.commit()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    name = request.form.get('name', '').strip()
    if not name:
        return redirect(url_for('index'))
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    session['user_id'] = user.id
    session['user_name'] = user.name
    return redirect(url_for('coach'))


@app.route('/coach')
def coach():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('coach.html', user_name=session.get('user_name', ''))


@app.route('/api/question')
def api_question():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'no_session'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'not_found'}), 404

    q = select_question(user)
    if not q:
        return jsonify({'error': 'no_questions'}), 404

    session['current_question_id'] = q.id

    return jsonify({
        'id': q.id,
        'content_area': q.content_area,
        'question_type': q.question_type,
        'thinking_level': q.thinking_level,
        'difficulty': q.difficulty,
        'stem_ar': q.stem_ar,
        'condition_ar': q.condition_ar,
        'col_a_ar': q.col_a_ar,
        'col_b_ar': q.col_b_ar,
        'choices': q.choices,
        'trap_tags': q.trap_tags,
    })


@app.route('/api/submit', methods=['POST'])
def api_submit():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'no_session'}), 401

    data = request.get_json()
    if not data:
        return jsonify({'error': 'bad_request'}), 400

    question_id = data.get('question_id')
    user_answer = data.get('answer')
    time_taken = int(data.get('time_taken', 0))

    user = User.query.get(user_id)
    question = Question.query.get(question_id)
    if not user or not question:
        return jsonify({'error': 'invalid_data'}), 400

    is_correct = check_answer(question, user_answer)
    feedback = generate_feedback(question, user_answer, is_correct)

    attempt = Attempt(
        user_id=user_id,
        question_id=question_id,
        user_answer_json=json.dumps(user_answer, ensure_ascii=False),
        is_correct=is_correct,
        time_taken_seconds=time_taken,
        error_type=None if is_correct else 'concept_error',
        coach_feedback=feedback,
    )
    db.session.add(attempt)
    update_user_stats(user, question, is_correct)

    return jsonify({
        'is_correct': is_correct,
        'feedback': feedback,
        'correct_answer': question.correct_answer,
        'solution_steps': question.solution_steps,
    })


@app.route('/api/progress')
def api_progress():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'no_session'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'not_found'}), 404

    attempts = Attempt.query.filter_by(user_id=user_id).all()
    total = len(attempts)
    correct = sum(1 for a in attempts if a.is_correct)

    by_area = {}
    for a in attempts:
        q = Question.query.get(a.question_id)
        if q:
            area = q.content_area
            by_area.setdefault(area, {'total': 0, 'correct': 0})
            by_area[area]['total'] += 1
            if a.is_correct:
                by_area[area]['correct'] += 1

    return jsonify({
        'name': user.name,
        'total_attempts': total,
        'correct': correct,
        'accuracy': round(correct / total * 100, 1) if total > 0 else 0,
        'by_area': by_area,
        'thinking_level': user.thinking_level,
        'content_levels': user.content_levels,
    })


if __name__ == '__main__':
    app.run(debug=True)
