from datetime import datetime
from functools import update_wrapper, wraps

from flask import (make_response,
                   redirect,
                   session,
                   url_for)

from digital_logic.experiment.service import get_current_assignment_session, \
    get_assignment


def nocache(func):  # pragma: no cover
    """
    Stop caching for pages wrapped in nocache decorator.
    """

    def new_func(*args, **kwargs):  # pragma: no cover
        resp = make_response(func(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp

    return update_wrapper(new_func, func)


def set_distractor_expired(assignment_session, allowed=300):
    expired = 0
    if assignment_session:
        now = datetime.utcnow()
        start = assignment_session.start_time
        expired = (now - start).total_seconds()
        session['distractor_seconds'] = expired
        session['distractor_timeout'] = [30 if session['debug_mode'] else 300][0]
    return expired


def set_expired(assignment):
    expired = 0
    if assignment:
        now = datetime.utcnow()
        start = assignment.created_on
        expired = (now - start).total_seconds()
        session['expired_seconds'] = expired
        session['assignment_timeout'] = assignment.expire_time
    return expired


def check_distractor_time(skip_redirect=False, allowed=300):
    def decorator(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            assignment_session = get_current_assignment_session()
            if assignment_session:
                expired = set_distractor_expired(assignment_session)
                if expired > allowed and not skip_redirect:
                    return redirect(url_for('exam.prediction_task'))
            return f(*args, **kwargs)
        return decorated_view
    return decorator


def check_time(skip_redirect=False):
    def decorator(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            assignment_id = session['current_assignment_id']
            assignment = get_assignment(assignment_id)
            allowed = assignment.expire_time

            if session['debug_mode']:
                allowed = 150

            if assignment:
                expired = set_expired(assignment)
                if expired > allowed and not skip_redirect:
                    return redirect(url_for('exp.timed_out'))

            return f(*args, **kwargs)
        return decorated_view
    return decorator

