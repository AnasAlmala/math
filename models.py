from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import json
import uuid

db = SQLAlchemy()


def gen_uuid():
    return str(uuid.uuid4())


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    name = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(5), default="ar")
    current_stage = db.Column(db.String(20), default="transition")
    # JSON: {"Arithmetic":4,"Algebra":4,"Geometry":2,"DataAnalysis":2}
    content_levels_json = db.Column(db.Text, default='{"Arithmetic":4,"Algebra":4,"Geometry":2,"DataAnalysis":2}')
    # JSON: {"QC":"medium","MC":"very_good","MA":"medium","NE":"good"}
    question_type_levels_json = db.Column(db.Text, default='{"QC":"medium","MC":"very_good","MA":"medium","NE":"good"}')
    thinking_level = db.Column(db.Integer, default=2)
    daily_drill_plan_json = db.Column(db.Text, default="{}")
    preferences_json = db.Column(db.Text, default="{}")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    attempts = db.relationship("Attempt", backref="user", lazy=True)
    snapshots = db.relationship("ProgressSnapshot", backref="user", lazy=True)

    @property
    def content_levels(self):
        return json.loads(self.content_levels_json)

    @content_levels.setter
    def content_levels(self, val):
        self.content_levels_json = json.dumps(val, ensure_ascii=False)

    @property
    def question_type_levels(self):
        return json.loads(self.question_type_levels_json)

    @question_type_levels.setter
    def question_type_levels(self, val):
        self.question_type_levels_json = json.dumps(val, ensure_ascii=False)

    @property
    def daily_drill_plan(self):
        return json.loads(self.daily_drill_plan_json)

    @daily_drill_plan.setter
    def daily_drill_plan(self, val):
        self.daily_drill_plan_json = json.dumps(val, ensure_ascii=False)


class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    source = db.Column(db.String(30), default="Custom")  # ETS/Manhattan/Custom
    content_area = db.Column(db.String(30), nullable=False)  # Arithmetic/Algebra/Geometry/DataAnalysis
    question_type = db.Column(db.String(5), nullable=False)  # QC/MC/MA/NE
    thinking_level = db.Column(db.Integer, nullable=False)  # 1-4
    difficulty = db.Column(db.Integer, default=3)  # 1-5
    trap_tags_json = db.Column(db.Text, default="[]")
    stem_ar = db.Column(db.Text, nullable=False)
    stem_en = db.Column(db.Text, nullable=True)
    condition_ar = db.Column(db.Text, nullable=True)  # for QC: shared condition
    col_a_ar = db.Column(db.Text, nullable=True)   # QC column A
    col_b_ar = db.Column(db.Text, nullable=True)   # QC column B
    choices_json = db.Column(db.Text, nullable=True)  # JSON array for MC/MA
    correct_answer_json = db.Column(db.Text, nullable=False)
    solution_steps_json = db.Column(db.Text, default="[]")
    concept_explanation = db.Column(db.Text, nullable=True)
    decision_explanation = db.Column(db.Text, nullable=True)
    common_mistakes_json = db.Column(db.Text, default="[]")
    is_example = db.Column(db.Boolean, default=False)

    attempts = db.relationship("Attempt", backref="question", lazy=True)

    @property
    def trap_tags(self):
        return json.loads(self.trap_tags_json)

    @property
    def choices(self):
        return json.loads(self.choices_json) if self.choices_json else None

    @property
    def correct_answer(self):
        return json.loads(self.correct_answer_json)

    @property
    def solution_steps(self):
        return json.loads(self.solution_steps_json)

    @property
    def common_mistakes(self):
        return json.loads(self.common_mistakes_json)

    def to_dict(self):
        return {
            "id": self.id,
            "source": self.source,
            "content_area": self.content_area,
            "question_type": self.question_type,
            "thinking_level": self.thinking_level,
            "difficulty": self.difficulty,
            "trap_tags": self.trap_tags,
            "stem_ar": self.stem_ar,
            "stem_en": self.stem_en,
            "condition_ar": self.condition_ar,
            "col_a_ar": self.col_a_ar,
            "col_b_ar": self.col_b_ar,
            "choices": self.choices,
            "correct_answer": self.correct_answer,
            "solution_steps": self.solution_steps,
            "concept_explanation": self.concept_explanation,
            "decision_explanation": self.decision_explanation,
            "common_mistakes": self.common_mistakes,
            "is_example": self.is_example,
        }


class Attempt(db.Model):
    __tablename__ = "attempts"
    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    question_id = db.Column(db.String(36), db.ForeignKey("questions.id"), nullable=False)
    user_answer_json = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    time_taken_seconds = db.Column(db.Integer, default=0)
    # concept_error / execution_error / reading_error / decision_error / None
    error_type = db.Column(db.String(20), nullable=True)
    error_details = db.Column(db.Text, nullable=True)
    coach_feedback = db.Column(db.Text, nullable=True)
    review_priority = db.Column(db.String(10), default="medium")  # high/medium/low
    session_id = db.Column(db.String(36), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def user_answer(self):
        return json.loads(self.user_answer_json)


class ProgressSnapshot(db.Model):
    __tablename__ = "progress_snapshots"
    id = db.Column(db.String(36), primary_key=True, default=gen_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    snapshot_date = db.Column(db.Date, default=date.today)
    accuracy_overall = db.Column(db.Float, default=0.0)
    accuracy_by_content_json = db.Column(db.Text, default="{}")
    accuracy_by_question_type_json = db.Column(db.Text, default="{}")
    accuracy_by_thinking_level_json = db.Column(db.Text, default="{}")
    most_common_error_types_json = db.Column(db.Text, default="[]")
    current_main_gap = db.Column(db.Text, nullable=True)
    next_recommended_focus = db.Column(db.Text, nullable=True)

    @property
    def accuracy_by_content(self):
        return json.loads(self.accuracy_by_content_json)

    @property
    def accuracy_by_question_type(self):
        return json.loads(self.accuracy_by_question_type_json)

    @property
    def accuracy_by_thinking_level(self):
        return json.loads(self.accuracy_by_thinking_level_json)

    def to_dict(self):
        return {
            "date": self.snapshot_date.isoformat(),
            "accuracy_overall": self.accuracy_overall,
            "accuracy_by_content": self.accuracy_by_content,
            "accuracy_by_question_type": self.accuracy_by_question_type,
            "accuracy_by_thinking_level": self.accuracy_by_thinking_level,
            "most_common_error_types": json.loads(self.most_common_error_types_json),
            "current_main_gap": self.current_main_gap,
            "next_recommended_focus": self.next_recommended_focus,
        }
