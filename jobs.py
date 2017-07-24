from datetime import datetime, timedelta
from redis import Redis
from rq import Queue

from digital_logic.core import mturk
from digital_logic.experiment.tasks import (check_for_start_assessment,
                                            approve_worker_assignments)
from scheduler import RQScheduler

redis_conn = Redis()
q = Queue(connection=redis_conn)
scheduler = RQScheduler(connection=Redis())


# This is mainly a test task job
def check_account_balance():
    job = q.enqueue_call(
        func=mturk.get_account_balance, args=(),
        result_ttl=5000)
    return job


def revoke_worker_qualification(worker_id, qual_type_id, reason):
    job = q.enqueue_call(
        func=mturk.revoke_qualification, args=(worker_id, qual_type_id, reason),
        result_ttl=5000
    )
    return job


def assign_worker_qualification(qual_type_id, worker_id, value,
                                send_notification):
    job = q.enqueue_call(
        func=mturk.assign_qualification,
        args=(qual_type_id, worker_id, value, send_notification),
        result_ttl=5000
    )
    return job


def approve_assignments():
    job = q.enqueue_call(
        func=approve_worker_assignments, args=(),
        result_ttl=5000
    )
    return job


def schedule_check_for_start_assessment(user_id, minutes=60):
    schedule = scheduler.enqueue_in(timedelta(minutes=minutes),
                                    check_for_start_assessment,
                                    args=(user_id,))
    return schedule


def schedule_account_balance():
    schedule = scheduler.schedule(
        scheduled_time=datetime.utcnow(),
        func=mturk.get_account_balance,
        interval=60,
        repeat=5,
        result_ttl=5000
    )
    return schedule


def schedule_approve_worker_assignments():
    schedule = scheduler.schedule(
        scheduled_time=datetime.utcnow(),
        func=approve_worker_assignments,
        interval=600,
        result_ttl=5000
    )
    return schedule


def schedule_periodic_check_for_start_assessment(subject_id):
    schedule = scheduler.schedule(
        scheduled_time=datetime.utcnow(),
        func=check_for_start_assessment,
        args=(subject_id,),
        interval=600,
        result_ttl=5000,
        repeat=10
    )
    return schedule
