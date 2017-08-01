from flask_security.utils import encrypt_password

from digital_logic.experiment.models import UserSubject as Subject, \
    SubjectAssignment

subject_data = {
    'mturk_worker_id': u'debugT7MSZ2',
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
             ('joe@mturk.com', 'password', ['mturk'], True),
             ('jack@mturk.com', 'password', ['mturk'], True),
             ('john@mturk.com', 'password', ['mturk'], True),
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
    subjects = [('debug5FQYY0', 2, 0,
                 'b9733ca6b41fec7402e5b014a826b2ed'),
                ('debugTU4D8C', 3, 1,
                 'ffe8e5f3447c73aac014e4612f3890da'),
                ('debugEBK0OZ', 4, 0,
                 'add6094c1d7eaa8bc2533c91472ff292'),
                ('debug6DB4LQ', 4, 0,
                 'add6094c1d7eaa8bc3434546567ff292')
                ]

    for s in subjects:
        subject = Subject(mturk_worker_id=s[0],
                          user_id=s[1],
                          experiment_group=s[2],
                          external_id=s[3])
        db.session.add(subject)
    db.session.commit()


def create_assignments(db):
    assignments = [(2, 'debug45678', 'debug45678', True, 3600),
                   (3, 'debug91234', 'debug91234', False, 1600),
                   (4, 'debug56789', 'debug56789', False, 3600)]
    for a in assignments:
        assignment = SubjectAssignment(subject_id=a[0],
                                       mturk_assignment_id=a[1],
                                       mturk_hit_id=a[2],
                                       is_complete=a[3],
                                       expire_time=a[4])
        db.session.add(assignment)
    db.session.commit()


def populate_data(ds):
    """
    Adapted from:
    https://github.com/mattupstate/flask-security/blob/develop/tests/utils.py
    """
    create_roles(ds)
    create_users(ds)
