from flask.ext.security.utils import encrypt_password


def create_roles(ds):
    """
    Adapted from:
    https://github.com/mattupstate/flask-security/blob/develop/tests/utils.py
    """
    for role in ('admin', 'subject'):
        ds.create_role(name=role)
    ds.commit()
    print('created roles')


def create_users(ds):
    """
    Adapted from:
    https://github.com/mattupstate/flask-security/blob/develop/tests/utils.py
    """
    users = [('mike@mike.com', 'password', ['admin'], True),
             ('joe@joe.com', 'password', ['subject'], True)
             ]

    for u in users:
        pw = u[1]
        if pw is not None:
            pw = encrypt_password(pw)
        roles = [ds.find_or_create_role(rn) for rn in u[2]]
        ds.commit()
        user = ds.create_user(email=u[0], password=pw, active=u[3])
        ds.commit()
        for role in roles:
            ds.add_role_to_user(user, role)
        ds.commit()


def populate_data(ds):
    """
    Adapted from:
    https://github.com/mattupstate/flask-security/blob/develop/tests/utils.py
    """
    create_roles(ds)
    create_users(ds)
