import os
import random
import string

from flask import current_app

from digital_logic.core import mturk


def make_database_url():
    return 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(
        os.getenv('DB_USER', 'postgres'),
        os.getenv('DB_PASSWORD', ''),
        os.getenv('DB_HOST', '127.0.0.1'),
        os.getenv('DB_PORT', '5432'),
        os.getenv('DB_NAME', 'experiment4'),
    )


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def subject_has_assessment_qualification(subject):
    workers = mturk.list_workers_with_qualification(
        current_app.config['MTURK_PT2_QUALIFICATION'])
    if subject.mturk_worker_id in workers:
        return True
    else:
        return False
