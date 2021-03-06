from datetime import datetime

from flask import current_app
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from ..core import db, mturk


class UserSubject(db.Model):
    __tablename__ = 'user_subjects'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    external_id = db.Column(db.String(128))
    mturk_worker_id = db.Column(db.String(128), nullable=False)
    skill_level = db.Column(db.String(50))
    age = db.Column(db.String(3))
    education = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    english_level = db.Column(db.String(50))
    experiment_group = db.Column(db.String(128))
    data_string = db.Column(db.Text())
    created_on = db.Column(db.DateTime(), default=datetime.utcnow())

    @classmethod
    def all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get(cls, id):
        return db.session.query(cls).filter(cls.id == id).one()

    @classmethod
    def get_by_mturk_worker_id(cls, mturk_worker_id):
        return db.session.query(cls).filter(
            cls.mturk_worker_id == mturk_worker_id).first()

    @classmethod
    def get_by_user_id(cls, user_id):
        return db.session.query(cls).filter(cls.user_id == user_id).first()


class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer(), primary_key=True)
    qb_id = db.Column(db.String(), unique=True, nullable=True)
    topic = db.Column(db.String(), nullable=False)
    data = db.Column(JSON(), nullable=False)
    level = db.Column(db.Integer(), nullable=False)

    @classmethod
    def get(cls, id):
        return db.session.query(cls).filter(cls.id == id).one()

    @classmethod
    def all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_random(cls):
        return db.session.query(cls).order_by(func.random()).first()

    @classmethod
    def get_by_qb_id(cls, qb_id):
        return db.session.query(cls).filter(cls.qb_id == qb_id).first()


class SubjectAssignment(db.Model):
    __tablename__ = 'subject_assignments'

    id = db.Column(db.Integer(), primary_key=True)
    subject_id = db.Column(db.Integer(), db.ForeignKey('user_subjects.id'),
                           nullable=False)

    mturk_assignment_id = db.Column(db.String(128), nullable=False)
    mturk_hit_id = db.Column(db.String(128), nullable=False)
    assignment_phase = db.Column(db.String(50))
    expire_time = db.Column(db.Integer(), nullable=False)
    ua_raw = db.Column(db.String(255))
    ua_browser = db.Column(db.String(128))
    ua_browser_version = db.Column(db.String(128))
    ua_os = db.Column(db.String(128))
    ua_os_version = db.Column(db.String(128))
    ua_device = db.Column(db.String(128))

    comments = db.Column(db.Text())
    did_cheat = db.Column(db.Boolean())
    did_timeout = db.Column(db.Boolean(),
                            nullable=False,
                            default=False)
    did_quit = db.Column(db.Boolean(),
                         nullable=False,
                         default=False)
    is_complete = db.Column(db.Boolean(),
                            nullable=False,
                            default=False)
    completed_on = db.Column(db.DateTime(),
                             nullable=True)
    exercise_pool = db.Column(ARRAY(db.Integer()))
    mastery = db.Column(ARRAY(db.Float()))

    mturk_completion_code = db.Column(db.String(255))
    mturk_assignment_status = db.Column(db.String(100))
    mturk_assignment_status_date = db.Column(db.DateTime())
    assignment_results = db.Column(JSON())
    assignment_predictions = db.Column(JSON())
    created_on = db.Column(db.DateTime(),
                           nullable=False,
                           default=datetime.utcnow())

    subject = db.relationship('UserSubject')

    responses = db.relationship('AssignmentResponse')

    @classmethod
    def get(cls, assignment_id):
        return db.session.query(cls).filter(cls.id == assignment_id).first()

    @classmethod
    def get_all_by_subject_id(cls, subject_id):
        return db.session.query(cls).filter(cls.subject_id == subject_id).all()

    @classmethod
    def get_by_subject_id(cls, subject_id):
        return db.session.query(cls).filter(cls.id == subject_id).first()

    @classmethod
    def get_lastest_by_subject_id(cls, subject_id, assignment_phase):
        query = db.session.query(cls).filter(
            cls.subject_id == subject_id).order_by(cls.created_on.desc())
        if assignment_phase:
            query = query.filter(cls.assignment_phase == assignment_phase)
        return query.first()

    @hybrid_property
    def total_answered(self):
        return len(self.responses)


class AssignmentResponse(db.Model):
    __tablename__ = 'assignment_responses'

    id = db.Column(db.Integer(), primary_key=True)
    assignment_id = db.Column(db.Integer(),
                              db.ForeignKey('subject_assignments.id'))
    exercise_id = db.Column(db.Integer(), db.ForeignKey('exercises.id'))
    selection = db.Column(db.Integer(), nullable=False)
    credit = db.Column(db.Float(), nullable=False, default=0.0)
    user_response_time = db.Column(db.Float, nullable=False, default=0.0)
    started_on = db.Column(db.DateTime(), nullable=False)
    completed_on = db.Column(db.DateTime(), default=datetime.utcnow())

    @classmethod
    def all_by_subject_id(cls, subject_id):
        return db.session.query(cls).filter(cls.id == subject_id).all()

    @classmethod
    def all_by_assignment_id(cls, assignment_id):
        return db.session.query(cls).filter(
            cls.assignment_id == assignment_id).all()


class AssignmentSession(db.Model):
    __tablename__ = 'assignment_sessions'

    id = db.Column(db.Integer(), primary_key=True)
    assignment_id = db.Column(db.Integer(),
                              db.ForeignKey('subject_assignments.id'))
    status = db.Column(db.String(100))
    start_time = db.Column(db.DateTime(), nullable=False,
                           default=datetime.utcnow())

    @classmethod
    def all_by_assignment_id(cls, assignment_id):
        return db.session.query(cls).filter(
            cls.assignment_id == assignment_id).all()

    @classmethod
    def get_lastest_by_assignment_id(cls, assignment_id):
        return db.session.query(cls).filter(
            cls.assignment_id == assignment_id).order_by(cls.start_time.desc())


class SparfaTrace(db.Model):
    __tablename__ = 'sparfa_trace'
    id = db.Column(db.Integer, primary_key=True)
    H = db.Column(db.PickleType, nullable=False)
    d = db.Column(db.PickleType, nullable=False)
    wmu = db.Column(db.PickleType, nullable=False)
    Gamma = db.Column(db.PickleType, nullable=False)
    question_ids = db.Column(db.PickleType, nullable=False)
