from functools import update_wrapper

from flask import make_response
from flask import session
from flask.ext.login import current_user

from digital_logic.experiment.models import AssignmentSession


def nocache(func):  # pragma: no cover
    """
    Stop caching for pages wrapped in nocache decorator.
    """

    def new_func(*args, **kwargs):  # pragma: no cover
        resp = make_response(func(*args, **kwargs))
        resp.cache_control.no_cache = True
        return resp

    return update_wrapper(new_func, func)


#
# def check_state(state, other=None):
#     def decorator(f):
#         @wraps(f)
#         def decorated_view(*args, **kwargs):
#             if current_user.is_authenticated:
#                 subject_session = get_subject_current_session(current_user.id)
#                 assignment = get_latest_assignment()
#                 if (not user_session and not state) or (user_session.status == state or user_session.status == other)):
#                     return f(*args, **kwargs)
#                 flash('This study is strictly sequential. '
#                       'Going back to redo a step is not allowed.',
#                       'warning')
#
# TODO: Finish check reading status
def check_reading_status(state, other=None):
    def decorator(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            if current_user.is_authenticated:
                assignment_id = session['current_assignment_id']
                current_session = AssignmentSession.get_latest_by_assignment_id(
                    assignment_id)

        return decorated_view
    return decorator
