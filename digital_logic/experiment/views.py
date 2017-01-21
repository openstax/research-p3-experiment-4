import logging

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
    logout_mturk_user)
from digital_logic.api.endpoints.textbook import render_textbook_text
from digital_logic.core import db
from digital_logic.exceptions import ExperimentError
from digital_logic.experiment.reading import reading_sections
from digital_logic.experiment.service import (
    get_latest_subject_assignment,
    all_subject_assignments,
    get_subject_by_user_id,
    add_session_record)
from digital_logic.experiment.forms import DemographyForm, FinalizeForm
from digital_logic.experiment.models import UserSubject as Subject
from digital_logic.experiment.models import SubjectAssignment
from digital_logic.helpers import parse_user_agent

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

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
    log.info('MTurk worker {0} loaded introduction page'.format(worker_id))

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
            latest_assignment = get_latest_subject_assignment(subject.id)

            if latest_assignment and latest_assignment.did_quit:
                raise ExperimentError('quit_experiment_early')
            elif latest_assignment and latest_assignment.is_complete:
                assignment = _login_and_prep_subject(worker_id,
                                                     assignment_id,
                                                     hit_id,
                                                     ua_dict,
                                                     debug_mode)
                session['current_assignment_id'] = assignment.id
            else:
                assignment = _login_and_prep_subject(worker_id,
                                                     assignment_id,
                                                     hit_id,
                                                     ua_dict,
                                                     debug_mode)
                session['current_assignment_id'] = assignment.id
                return redirect(url_for('exp.demography'))
        else:
            raise ExperimentError('experiment_completed')

    # If no subject is found create one and enter the experiment
    if not subject:
        assignment = _login_and_prep_subject(worker_id,
                                             assignment_id,
                                             hit_id,
                                             ua_dict,
                                             debug_mode)
        session['current_assignment_id'] = assignment.id
        return redirect(url_for('exp.demography'))


@exp.route('/demography', methods=['GET', 'POST'])
def demography():
    subject = get_subject_by_user_id(current_user.id)
    assignment = SubjectAssignment.get(
        session['current_assignment_id'])

    form = DemographyForm(request.form)

    if form.validate_on_submit():
        form.populate_obj(subject)
        db.session.add(subject)
        add_session_record(assignment.id, 'Reading')
        db.session.commit()
        return redirect(url_for('exp.reading'))

    return render_template('demography.html', form=form)


@exp.route('/reading', methods=['GET'])
def reading():
    section = None
    text = None

    if 'reading_sections' not in session or not session['reading_sections']:
        sections_completed = 0
        total_sections = len(reading_sections)

        session['reading_sections'] = reading_sections
        session['sections_completed'] = sections_completed
        session['total_sections'] = total_sections

        section = session['reading_sections'][sections_completed]
    else:
        session['sections_completed'] += 1
        if session['sections_completed'] < session['total_sections']:
            section = session['reading_sections'][session['sections_completed']]
        else:
            return redirect(url_for('exp.finalize'))

    text = render_textbook_text(section)

    return render_template('reading.html', text=text)


@exp.route('/finalize', methods=['GET', 'POST'])
def finalize():
    form = FinalizeForm()
    return render_template('finalize.html', form=form)


@exp.route('/assessment', methods=['GET', 'POST'])
def assessment_index():
    return 'assessment_index!'
