from flask_security.utils import encrypt_password

from digital_logic.experiment.models import UserSubject as Subject

subject_data = {
    'assignment_id': u'debugSIP7SD',
    'worker_id': u'debugT7MSZ2',
    'hit_id': u'debugVY4J2G',
    'experiment_group': u'test',
}


def subject_data_copy():
    data = dict()
    data.update(subject_data)
    return data


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


def create_subjects(db):
    # assignment_id, worker_id, hit_id, group_num, external_id, status
    subjects = [('debug28VFCH', 'debug5FQYY0', 'debug8O8WX0', 0,
                 'b9733ca6b41fec7402e5b014a826b2ed', 'QUITEARLY'),
                ('debug07N3PA', 'debugTU4D8C', 'debug8RIZSB', 1,
                 'ffe8e5f3447c73aac014e4612f3890da', 'COMPLETED'),
                ('debug5FQYY0', 'debugEBK0OZ', 'debugN3WMIY', 0,
                 'add6094c1d7eaa8bc2533c91472ff292', 'GARBAGE')]

    for s in subjects:
        subject = Subject(assignment_id=s[0],
                          worker_id=s[1],
                          hit_id=s[2],
                          experiment_group=s[3],
                          external_id=s[4],
                          status=s[5])
        db.session.add(subject)
    db.session.commit()


def populate_data(ds):
    """
    Adapted from:
    https://github.com/mattupstate/flask-security/blob/develop/tests/utils.py
    """
    create_roles(ds)
    create_users(ds)
