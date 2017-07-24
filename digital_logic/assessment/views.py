import logging
from datetime import datetime

from flask import (Blueprint,
                   redirect,
                   render_template,
                   request,
                   session,
                   url_for)
from flask import current_app as app
from flask_login import current_user

from digital_logic.accounts.auth import logout_mturk_user, \
    _login_and_prep_subject, mturk_permission
from digital_logic.core import db
from digital_logic.decorators import check_distractor_time, check_time
from digital_logic.exceptions import ExperimentError
from digital_logic.experiment.exercise import (next_exercise_from_pool,
                                               get_assignment_next_exercise)
from digital_logic.experiment.forms import PredictionsForm, FinalizeForm
from digital_logic.experiment.service import (
    all_subject_assignments,
    get_latest_subject_assignment,
    save_session_record,
    get_assignment,
    save_assignment_predictions,
    get_subject_by_user_id,
    get_exercise,
    save_assignment_response,
    get_current_assignment_session)
from digital_logic.helpers import parse_user_agent
from digital_logic.models import UserSubject as Subject
from digital_logic.utils import id_generator

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
    assignment_phase = 'Assessment'

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

        if len(assignments) < len(
                app.config['ASSIGNMENT_PHASES']) or debug_mode:
            latest_assignment = get_latest_subject_assignment(subject.id,
                                                              assignment_phase)

            if not debug_mode and (
                latest_assignment and latest_assignment.did_quit):
                raise ExperimentError('quit_experiment_early')
            elif not debug_mode and (
                latest_assignment and latest_assignment.is_complete):
                raise ExperimentError('phase_completed')
            else:
                assignment = _login_and_prep_subject(worker_id,
                                                     assignment_id,
                                                     hit_id,
                                                     ua_dict,
                                                     assignment_phase,
                                                     debug_mode)
                if not assignment:
                    raise ExperimentError('quit_experiment_early')
                else:
                    session['current_assignment_id'] = assignment.id

                    save_session_record(assignment.id, 'Distracting')
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
        save_session_record(assignment.id, 'Distracting')
        return redirect(url_for('exam.distractor_task'))


@exam.route('/distractor', methods=['GET'])
@mturk_permission.require()
@check_time(allowed=1800)
@check_distractor_time()
def distractor_task():
    return render_template('distracting.html')


@exam.route('/predicting', methods=['GET', 'POST'])
@mturk_permission.require()
@check_time(allowed=1800)
def prediction_task():
    form = PredictionsForm(request.form)
    assignment = get_assignment(session['current_assignment_id'])
    if request.method == 'GET':
        exp_session = get_current_assignment_session()
        if exp_session.status is not 'Predicting':
            save_session_record(assignment.id, 'Predicting')
    if form.validate_on_submit():
        prediction_results = dict(assignment_id=assignment.id,
                                  basic_recall=form.basics.data,
                                  expressions=form.expressions.data,
                                  circuits=form.circuits.data,
                                  truth_tables=form.truth_tables.data,
                                  overall=form.overall.data
                                  )
        save_assignment_predictions(assignment.id, prediction_results)
        save_session_record(assignment.id, 'Assessment')
        return redirect(url_for('exam.next_exercise'))

    return render_template('predicting.html', form=form)


@exam.route('/exercise/next')
@mturk_permission.require()
@check_time(allowed=1800)
def next_exercise():
    assignment = get_assignment(session['current_assignment_id'])
    total_exercises = len(assignment.exercise_pool)
    answered_exercises = session.get('answered_exercises', 0)

    if 'answered_exercises' not in session or not session['answered_exercises']:
        session['answered_exercises'] = answered_exercises
        session['total_exercises'] = total_exercises
        session['exercises_correct'] = 0
        session['exercises_incorrect'] = 0

    elif session['answered_exercises'] == total_exercises:
        return redirect(url_for('exam.finalize'))

    exercise = get_assignment_next_exercise(assignment)
    session['current_exercise_id'] = exercise.id
    session['exercise_start'] = datetime.utcnow()

    return render_template('exam_exercise.html',
                           feedback=False,
                           total_exercises=total_exercises,
                           answered_exercises=answered_exercises,
                           exercise=exercise.data['simple_question'])


@exam.route('/response', methods=['POST'])
@mturk_permission.require()
@check_time(allowed=1800)
def submit_response():
    exercise = get_exercise(session['current_exercise_id'])
    assignment = get_assignment(session['current_assignment_id'])
    started_on = session['exercise_start']

    answer = request.form.get('choice', None)

    if answer:
        session['last_answer'] = int(answer)
        credit = float(
            exercise.data['simple_question']['answer_choices'][int(answer)][
                'credit'])

        save_assignment_response(assignment.id, exercise.id, credit, answer,
                                 started_on)
        if credit == 0:
            session['exercises_incorrect'] += 1
        else:
            session['exercises_correct'] += 1

        session['answered_exercises'] += 1
    return redirect(url_for('exam.next_exercise'))


@exam.route('/finalize', methods=['GET', 'POST'])
@mturk_permission.require()
def finalize():
    form = FinalizeForm()
    assignment = get_assignment(session['current_assignment_id'])
    if form.validate_on_submit():
        form.populate_obj(assignment)
        # TODO: move this to its own function
        assignment_results = dict()
        correct = session['exercises_correct']
        incorrect = session['exercises_incorrect']
        total = session['total_exercises']
        score = ((float(correct)) / total) * 100

        assignment_results['correct'] = correct
        assignment_results['incorrect'] = incorrect
        assignment_results['total'] = total
        assignment_results['score'] = score
        assignment_results['phase'] = assignment.assignment_phase

        log.info('A score of {0} was recorded for subject {1}'.format(
            score,
            assignment.subject_id))

        assignment.mturk_completion_code = id_generator()
        assignment.is_complete = True
        assignment.assignment_results = assignment_results
        db.session.add(assignment)
        save_session_record(assignment.id, 'Completed')

        db.session.commit()

        return redirect(url_for('exp.summary'))

    return render_template('exam_finalize.html', form=form)
