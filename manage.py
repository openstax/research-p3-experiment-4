import os
import random
import string
import sys
from datetime import datetime

import click

from flask import current_app
from flask_security import utils

from digital_logic import create_app
from digital_logic.core import db

app = create_app()


def random_id_generator(size=6, chars=string.ascii_uppercase +
                                      string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def create_debug_url(base_url, worker_id=None):
    if worker_id:
        worker_id=worker_id
    else:
        worker_id = random_id_generator()
    hit_id = random_id_generator()
    assignment_id = random_id_generator()

    info = dict(base_url=base_url,
                worker_id=worker_id,
                hit_id=hit_id,
                assignment_id=assignment_id)

    launch_url = ('{base_url}?worker_id=debug{worker_id}'
                  '&hit_id=debug{hit_id}'
                  '&assignment_id=debug{assignment_id}'
                  '&mode=debug'.format(**info))
    return launch_url


@app.cli.command()
def list_routes():
    """ List available routes in the application."""
    output = []
    for rule in current_app.url_map.iter_rules():

        methods = ','.join(rule.methods)
        url = str(rule)
        if '_debug_toolbar' in url:
            continue
        line = "{:50s} {:30s} {}".format(rule.endpoint, methods, url)
        output.append(line)

    click.echo('\n'.join(sorted(output)))


@app.cli.command()
@click.confirmation_option(
    prompt='This will erase everything in the database. Do you want to continue?')
def reset_db():
    """Resets the database to the original state using 
    alembic downgrade and upgrade commands"""
    from alembic.command import downgrade, upgrade
    from alembic.config import Config as AlembicConfig
    config = AlembicConfig('alembic.ini')
    downgrade(config, 'base')
    upgrade(config, 'head')
    print('Database has been reset')


@app.cli.command()
@click.option('--email', prompt=True)
@click.password_option('--password')
def create_admin_user(email, password):
    """Create an admin user to be used to login to the database initially."""
    user_datastore = current_app.extensions['security'].datastore
    user_datastore.find_or_create_role(name='admin',
                                       description='Administrator')
    encrypted_password = utils.encrypt_password(password)

    if not user_datastore.get_user(email):
        user_datastore.create_user(email=email,
                                   active=True,
                                   registered_at=datetime.now(),
                                   confirmed_at=datetime.now(),
                                   password=encrypted_password)
    db.session.commit()
    user_datastore.add_role_to_user(email, 'admin')
    db.session.commit()


@app.cli.command()
def send_test_email():
    """Send a test email."""
    from flask_mail import Message
    from digital_logic.core import mail

    to = ['labs@openstax.org']
    subject = 'Test Email'
    template = '<h1>This is a test of Openstax Labs email messaging system</h1>'

    msg = Message(
        subject,
        recipients=to,
        html=template,
        sender=current_app.config['SECURITY_EMAIL_SENDER']
    )
    mail.send(msg)


@app.cli.command()
def debug_urls():
    practice_url = create_debug_url('http://localhost:2992/exp/')
    worker_id = practice_url.split('?')[1].split('&')[0].split('debug')[1]
    assessment_url = create_debug_url('http://localhost:2992/exam', worker_id)

    print('practice_url: {}'.format(practice_url))
    print('assessment_url: {}'.format(assessment_url))

@app.cli.command()
@click.option('--web/--no-web',
              default=True,
              help="Whether or not to run the flask dev server")
@click.option('--worker/--no-worker',
              default=True,
              help="Whether or not to run the worker process")
@click.option('--sched/--no-sched',
              default=True,
              help="Whether or not to run the scheduler process")
@click.option('--webpack/--no-webpack',
              default=True,
              help="Whether or not to run the webpack dev server")
def devserver(web, worker, sched, webpack):
    """
    Run the flask development server, workers, and scheduler
    """
    try:
        from honcho.manager import Manager
    except ImportError:
        raise click.ClickException(
            'cannot import honcho: did you run `pip install -e .` ?'
        )

    os.environ['PYTHONUNBUFFERED'] = 'true'

    m = Manager()

    if web:
        m.add_process('web', 'python wsgi.py')

    if worker:
        m.add_process('worker', 'python worker.py')

    if sched:
        m.add_process('sched', 'python scheduler.py')

    if webpack:
        m.add_process('webpack', 'npm run start')

    m.loop()

    sys.exit(m.returncode)


if __name__ == '__main__':
    app.cli()
