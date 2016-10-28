import random

from collections import Counter
from datetime import datetime

from ..core import db


def get_experiment_group(num_groups):
    """
    This will take a number of conditions and counter-balance the number of
    subjects in each condition.
    :param num_groups: (int) number of groups
    :return: group
    """
    counts = Counter()

    subjects = db.session.query(Subject)\
        .filter(Subject.status == 'COMPLETED')\
        .all()

    for cond in range(num_groups):
        counts[cond] = 0

    for subject in subjects:
        counts[subject.experiment_group] += 1

    min_count = min(counts.values())

    minimums = [hash for hash, count in counts.items() if count == min_count]

    return random.choice(minimums)


def create_subject(data):
    subject = Subject(**data)
    db.session.add(subject)
    db.session.commit()

    return subject


def update_subject(subject_id, data):
    subject = Subject.get(subject_id)

    for k, v in data.items():
        setattr(subject, k, v)

    db.session.add(subject)
    db.session.commit()

    return subject


class Subject(db.Model):
    __tablename__ = 'subjects'
    __table_args__ = (db.UniqueConstraint('assignment_id', 'worker_id',
                                          name='worker_id_assignment_id_uix'),)

    id = db.Column(db.Integer(), primary_key=True)
    external_id = db.Column(db.String(128))
    assignment_id = db.Column(db.String(128), nullable=False)
    worker_id = db.Column(db.String(128), nullable=False)
    hit_id = db.Column(db.String(128), nullable=False)
    ua_raw = db.Column(db.String(128))
    ua_browser = db.Column(db.String(128))
    ua_browser_version = db.Column(db.String(128))
    ua_os = db.Column(db.String(128))
    ua_os_version = db.Column(db.String(128))
    ua_device = db.Column(db.String(128))
    status = db.Column(db.String(128))
    experiment_group = db.Column(db.String(128))
    data_string = db.Column(db.Text())
    created_on = db.Column(db.DateTime(), default=datetime.utcnow())
    completion_code = db.Column(db.String(128))

    @classmethod
    def all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get(cls, id):
        return db.session.query(cls).filter(cls.id == id).one()

    @classmethod
    def get_by_worker_id(cls, worker_id):
        return db.session.query(cls).filter(cls.worker_id == worker_id).first()
