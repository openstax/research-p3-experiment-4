import click
from datetime import datetime

from flask import current_app
from flask_security import utils

from digital_logic import create_app
from digital_logic.core import db

app = create_app()


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
@click.confirmation_option(prompt='This will erase everything in the database. Do you want to continue?')
def reset_db():
    """Resets the database to the original state using alembic downgrade and upgrade commands"""
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


if __name__ == '__main__':
    app.cli()
