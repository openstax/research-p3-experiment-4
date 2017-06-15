import json
import logging

from datetime import datetime

from flask import (Blueprint,
                   render_template,
                   request,
                   session,
                   current_app as app)
from flask import redirect
from flask import url_for
from flask_login import current_user

from digital_logic.accounts.auth import (
    _login_and_prep_subject,
    logout_mturk_user,
    mturk_permission)
from digital_logic.experiment.reading import render_textbook_text
from digital_logic.core import db
from digital_logic.decorators import check_time
from digital_logic.exceptions import ExperimentError
from digital_logic.experiment._constants import DEFAULT_E_NUM
from digital_logic.experiment.exercise import get_assignment_next_exercise
from digital_logic.experiment.reading import reading_sections, get_section_obj
from digital_logic.experiment.service import (
    get_latest_subject_assignment,
    all_subject_assignments,
    get_subject_by_user_id,
    save_session_record,
    get_exercise,
    get_assignment,
    save_assignment_response,
    qualify_assignment)
from digital_logic.experiment.forms import DemographyForm, FinalizeForm
from digital_logic.experiment.models import UserSubject as Subject
from digital_logic.experiment.models import SubjectAssignment
from digital_logic.helpers import parse_user_agent
from digital_logic.utils import id_generator

__logs__ = logging.getLogger(__name__)

exp = Blueprint('exp',
                __name__,
                url_prefix='/exp',
                template_folder='../templates/experiment')


@exp.errorhandler(ExperimentError)
def error_handler(exception):
    return exception.error_page(request)


@exp.route('/')
def introduction():
    """
    Shows the introduction page to the experiment. The mturk worker agrees to
    participate in the experiment from this page. They are redirected here
    from the consent form on Amazon Mechanical Turk.

    The following values should be received from the url params:

    :hit_id: the identifier of the human intelligence task (HIT)
    :worker_id: the identifier of the worker in mturk
    :assignment_id: the identifier of the assignment
    :mode: the mode of the experiment

    if the assignment_id is not received the introduction template will hide the
    begin experiment button.

    :return: the rendered introduction template
    """
    hit_id = request.values.get('hit_id', None)
    assignment_id = request.values.get('assignment_id', None)
    worker_id = request.values.get('worker_id', None)
    mode = request.values.get('mode', None)
    __logs__.info(
        'MTurk worker {0} loaded practice introduction page'.format(worker_id))

    return render_template('introduction.html',
                           assignment_id=assignment_id,
                           hit_id=hit_id,
                           worker_id=worker_id,
                           mode=mode)


@exp.route('/start', methods=['GET'])
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
    3. If the mode is debug the subject data is allowed to be overwritten in the
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
    assignment_phase = 'Practice'

    ua_dict = parse_user_agent(request.headers.get('User-Agent'))

    subject = Subject.get_by_mturk_worker_id(worker_id)

    __logs__.info(
        'MTurk worker {} attempting to start the experiment'.format(worker_id))

    if mode == 'debug':
        debug_mode = True
    else:
        debug_mode = False

    __logs__.info('debug mode is {0}'.format(debug_mode))

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
                    save_session_record(assignment.id, 'Started')
                    return redirect(url_for('exp.demography'))
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
        save_session_record(assignment.id, 'Started')
        return redirect(url_for('exp.demography'))


@exp.route('/demography', methods=['GET', 'POST'])
@mturk_permission.require()
@check_time()
def demography():
    subject = get_subject_by_user_id(current_user.id)
    assignment = SubjectAssignment.get(session['current_assignment_id'])

    form = DemographyForm(request.form)

    if form.validate_on_submit():
        form.populate_obj(subject)
        db.session.add(subject)
        save_session_record(assignment.id, 'Reading')
        db.session.commit()
        return redirect(url_for('exp.reading'))

    return render_template('demography.html', form=form)


@exp.route('/reading/next', methods=['GET', 'POST'])
@mturk_permission.require()
@check_time()
def reading():
    text = None

    subject = get_subject_by_user_id(current_user.id)

    section = request.form.get('section', None)

    if 'current_section' not in session or not session['current_section']:
        sections_completed = 0
        total_sections = len(reading_sections)

        session['sections_completed'] = sections_completed
        session['total_sections'] = total_sections

        section_obj = get_section_obj('preface')

        session['current_section'] = section_obj
        session['last_section'] = section_obj['name']
    elif 'last_section' in session and session['last_section'] == section:
        section_obj = get_section_obj(session['last_section'])
    else:
        section_obj = session['current_section']
        session['sections_completed'] += 1
        if session['sections_completed'] < session['total_sections']:
            section_obj = get_section_obj(
                session['current_section']['next_section'])
            session['current_section'] = section_obj
            session['last_section'] = section_obj['name']
        else:
            if int(subject.experiment_group) == 2:
                save_session_record(session['current_assignment_id'],
                                    'Distracting')
                return redirect(url_for('exam.distractor_task'))
            save_session_record(session['current_assignment_id'],
                                'Finalizing')
            return redirect(url_for('exp.finalize'))

    session['is_reading'] = True
    text = render_textbook_text(section_obj['name'])
    return render_template('reading.html',
                           text=text,
                           section=section_obj,
                           subject_id=subject.id)


@exp.route('/exercise/next', methods=['GET', 'POST'])
@mturk_permission.require()
@check_time()
def next_exercise():
    assignment = get_assignment(session['current_assignment_id'])
    total_exercises = DEFAULT_E_NUM
    answered_exercises = session.get('answered_exercises', 0)

    if 'answered_exercises' not in session or not session['answered_exercises']:
        session['answered_exercises'] = answered_exercises
        session['total_exercises'] = total_exercises
        session['exercises_correct'] = 0
        session['exercises_incorrect'] = 0

    if not session['is_reading'] and session['answered_exercises'] == 6:
        return redirect(
            '{0}?{1}'.format(url_for('exp.reading'), 'status=complete'))

    if session['answered_exercises'] == total_exercises:
        return redirect(
            '{0}?{1}'.format(url_for('exp.reading'), 'status=complete'))

    if 'last_answer' in session and session['last_answer']:
        exercise = get_exercise(session['current_exercise_id'])
    else:

        session['is_reading'] = False

        exercise = get_assignment_next_exercise(assignment)
        session['current_exercise_id'] = exercise.id
        session['exercise_start'] = datetime.utcnow()

    return render_template('exercise.html',
                           feedback=False,
                           total_exercises=total_exercises,
                           answered_exercises=answered_exercises,
                           exercise=exercise.data['simple_question'])


@exp.route('/response', methods=['POST'])
@mturk_permission.require()
@check_time()
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
        return redirect(url_for('exp.show_feedback'))
    else:
        return redirect(url_for('exp.next_exercise'))


@exp.route('/feedback', methods=['GET', 'POST'])
@mturk_permission.require()
@check_time()
def show_feedback():
    if request.method == 'POST' or (
                    'skip_feedback' in session and session['skip_feedback']):
        session['current_exercise_id'] = None
        session['exercise_start'] = None
        session['last_answer'] = None
        return redirect(url_for('exp.next_exercise'))

    assignment = get_assignment(session['current_assignment_id'])
    answered_exercises = session['answered_exercises']
    total_exercises = session['total_exercises']
    exercise = get_exercise(session['current_exercise_id'])
    choices = exercise.data['simple_question']['answer_choices']
    correct_choices = [i for i, c in enumerate(choices) if
                       float(c['credit']) > 0]
    incorrect_choices = [i for i, c in enumerate(choices) if
                         float(c['credit']) == 0]

    answer = session['last_answer']
    correct_answer = answer in correct_choices

    return render_template('exercise.html',
                           feedback=True,
                           answer=answer,
                           correct_answer=correct_answer,
                           answered_exercises=answered_exercises,
                           total_exercises=total_exercises,
                           correct_choices=correct_choices,
                           incorrect_choices=incorrect_choices,
                           exercise=exercise.data['simple_question']
                           )


@exp.route('/finalize', methods=['GET', 'POST'])
@mturk_permission.require()
def finalize():
    from jobs import (assign_worker_qualification,
                      schedule_check_for_start_assessment)
    PART_2_QUAL = app.config['MTURK_PT2_QUALIFICATION']
    DLOGIC_QUAL = app.config['MTURK_DL_QUALIFICATION']

    form = FinalizeForm()
    assignment = get_assignment(session['current_assignment_id'])
    if form.validate_on_submit():
        form.populate_obj(assignment)
        subject = get_subject_by_user_id(current_user.id)
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

        __logs__.info('A score of {0} was recorded for subject {1}'.format(
            score,
            assignment.subject_id))

        assignment.mturk_completion_code = id_generator()
        assignment.is_complete = True
        assignment.assignment_results = assignment_results
        db.session.add(assignment)
        save_session_record(assignment.id, 'Completed')

        db.session.commit()

        qualified = qualify_assignment(assignment.id)

        if qualified:
            assign_worker_qualification(PART_2_QUAL, subject.mturk_worker_id, 1,
                                        True)
            schedule_check_for_start_assessment(current_user.id)

        assign_worker_qualification(DLOGIC_QUAL, subject.mturk_worker_id, 1,
                                    True)

        return redirect(url_for('exp.summary'))

    return render_template('finalize.html', form=form)


@exp.route('/summary', methods=['GET'])
@mturk_permission.require()
def summary():
    # TODO: Finish summary page
    qualified = False

    assignments = all_subject_assignments(session['current_subject_id'])

    current_assignment = get_assignment(session['current_assignment_id'])

    completion_code = current_assignment.mturk_completion_code

    if (current_assignment.assignment_phase == 'Practice'
        and current_assignment.mturk_assignment_status == 'Accepted'):
        qualified = True

    return render_template('summary.html',
                           assignments=assignments,
                           completion_code=completion_code,
                           qualified=qualified)


@exp.route('/timeout', methods=['GET', 'POST'])
def timed_out():
    assignment = get_assignment(session['current_assignment_id'])
    if request.method == 'POST':
        assignment.did_timeout = True
        db.session.add(assignment)
        save_session_record(assignment.id, 'Finalizing')
        db.session.commit()
        return redirect(url_for('exp.finalize'))
    return render_template('timeout.html')
