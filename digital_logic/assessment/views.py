import logging

from flask import Blueprint, render_template, request
from flask import current_app as app
from flask import redirect
from flask import session
from flask import url_for
from flask_login import current_user

from digital_logic.accounts.auth import logout_mturk_user, \
    _login_and_prep_subject, mturk_permission
from digital_logic.exceptions import ExperimentError
from digital_logic.experiment.service import all_subject_assignments, \
    get_latest_subject_assignment, add_session_record
from digital_logic.helpers import parse_user_agent
from digital_logic.models import UserSubject as Subject

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

exam = Blueprint('exam',
                 __name__,
                 url_prefix='/exam',
                 template_folder='../templates/assessment')


@exam.route('/')
def exam_index():
    hit_id = request.values.get('hit_id', None)
    assignment_id = request.values.get('assignment_id', None)
    worker_id = request.values.get('worker_id', None)
    mode = request.values.get('mode', None)
    log.info('MTurk worker {0} loaded exam introduction page'.format(worker_id))

    return render_template('exam_intro.html',
                           assignment_id=assignment_id,
                           hit_id=hit_id,
                           worker_id=worker_id,
                           mode=mode)


@exam.route('/start', methods=['GET'])
def start():
    """
    When the worker is ready to start the experiment this route is called
    from a new window when `Begin` is pressed on the introduction screen. The
    `Begin` button is linked to a javascript click event that loads a new window
    calling this route with the correct GET request params.

    If all is successful several things happen:

    1. A subject is looked up based on the worker_id to see if they have done
    this experiment before. If they have they are redirected.
    2. If the mturk_worker_id is unique their browser user agent is parsed and
    a new `Subject` and `SubjectAssignment` is created in the database.
    3. If the mode is debug the subject is allowed to be overwritten in the
    database.

    Required GET request params:

    :hit_id: the identifier of the human intelligence task (HIT)
    :worker_id: the identifier of the worker in mturk
    :assignment_id: the identifier of the assignment in mturk

    Optional GET request params:
    :debug: the mode of the experiment
    """
    # Ensure we get the all the required params
    if not (('hit_id' in request.args) and ('assignment_id' in request.args) and
                ('worker_id' in request.args)):
        raise ExperimentError('incorrect_experiment_params')

    if current_user.is_authenticated:
        session.clear()
        logout_mturk_user()

    # Assign get params to vars
    worker_id = request.args.get('worker_id')
    assignment_id = request.args.get('assignment_id')
    hit_id = request.args.get('hit_id')
    mode = request.args.get('mode', None)
    assignment_phase = ''

    ua_dict = parse_user_agent(request.headers.get('User-Agent'))

    subject = Subject.get_by_mturk_worker_id(worker_id)

    log.info(
        'MTurk worker {} attempting to start the experiment'.format(worker_id))

    if mode == 'debug':
        debug_mode = True
    else:
        debug_mode = False

    log.info('debug mode is {0}'.format(debug_mode))

    if subject:
        assignments = all_subject_assignments(subject.id)

        if len(assignments) < len(app.config['ASSIGNMENT_PHASES']):
            latest_assignment = get_latest_subject_assignment(subject.id,
                                                              assignment_phase)

            if not debug_mode and (latest_assignment and latest_assignment.did_quit):
                raise ExperimentError('quit_experiment_early')
            elif not debug_mode and (latest_assignment and latest_assignment.is_complete):
                raise ExperimentError('phase_completed')
            else:
                assignment = _login_and_prep_subject(worker_id,
                                                     assignment_id,
                                                     hit_id,
                                                     ua_dict,
                                                     assignment_phase,
                                                     debug_mode)
                session['current_assignment_id'] = assignment.id
                add_session_record(assignment.id, 'Started')
                return redirect(url_for('exam.distractor_task'))
        else:
            raise ExperimentError('experiment_completed')
    else:
        # If no subject is found create one and enter the experiment
        assignment = _login_and_prep_subject(worker_id,
                                             assignment_id,
                                             hit_id,
                                             ua_dict,
                                             assignment_phase,
                                             debug_mode)
        session['current_assignment_id'] = assignment.id
        add_session_record(assignment.id, 'Started')
        return redirect(url_for('exam.distractor_task'))


@exam.route('/distractor', methods=['GET', 'POST'])
def distractor_task():
    session['distractor_seconds'] = 600
    return render_template('distracting.html')


@exam.route('/predicting', methods=['GET'])
@mturk_permission.require()
def prediction_task():
    return 'Predicting how well i will do at the pageant'


@exam.route('/assessment')
@mturk_permission.require()
def testing():
    return 'Testing ... Testing ... 1 - 2 - 3'
