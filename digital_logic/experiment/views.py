from flask import (Blueprint,
                   render_template,
                   request)

from digital_logic.core import db
from digital_logic.exceptions import ExperimentError
from digital_logic.experiment.models import Subject, create_subject, \
    get_experiment_group
from digital_logic.helpers import parse_user_agent, make_external_id

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
    2. If the mturk worker_id is unique their browser user agent is parsed and
    a new `Subject` is created in the database.
    3. If the mode is debug the subject is allowed to be overwritten in the
    database

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

    worker_id = request.args.get('worker_id')
    assignment_id = request.args.get('assignment_id')
    hit_id = request.args.get('hit_id')
    mode = request.args.get('mode', None)
    ua_dict = parse_user_agent(request.headers.get('User-Agent'))

    subject = Subject.get_by_worker_id(worker_id)

    data = dict(worker_id=worker_id,
                assignment_id=assignment_id,
                hit_id=hit_id)

    data = {**data, **ua_dict}

    if mode == 'debug':
        debug_mode = True
    else:
        debug_mode = False

    # If the subject exists and debug is True
    # clear subject's data and load the experiment
    if subject and debug_mode:
        subject.data_string = ''
        db.session.add(subject)
        db.session.commit()
        return render_template('start.html',
                               subject_id=subject.id,
                               mode=mode)

    # If the subject exists and debug is False
    if subject and not debug_mode:
        # Check to see their status is completed
        if subject.status == 'COMPLETED':
            raise ExperimentError('experiment_completed')
        elif subject.status == 'QUITEARLY' or subject.status == 'STARTED':
            raise ExperimentError('quit_experiment_early')
        else:
            raise ExperimentError('unknown_status')

    # If no subject is found create one and enter the experiment
    if not subject:
        # Add an external_id so we can send the subject to other systems.
        data['external_id'] = make_external_id(data['worker_id'],
                                               data['assignment_id'],
                                               data['hit_id'])

        data['experiment_group'] = get_experiment_group(2)
        data['status'] = 'STARTED'

        new_subject = create_subject(data)
        return render_template('start.html',
                               subject_id=new_subject.id,
                               mode=mode)
