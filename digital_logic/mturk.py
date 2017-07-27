from boto.mturk.connection import MTurkConnection, MTurkRequestError
import logging


class MTurkHIT(object):
    """ Structure for dealing with MTurk HITs """

    def __init__(self, json_options):
        self.options = json_options

    def __repr__(self):
        for opt in self.options:
            self.options[opt] = self.options[opt].encode('ascii', 'replace')
        return "%s \n\tStatus: %s \n\tHITid: %s \
            \n\tmax:%s/pending:%s/complete:%s/remain:%s \n\tCreated:%s \
            \n\tExpires:%s\n" % (
            self.options['title'],
            self.options['status'],
            self.options['hitid'],
            self.options['max_assignments'],
            self.options['number_assignments_pending'],
            self.options['number_assignments_completed'],
            self.options['number_assignments_available'],
            self.options['creation_time'],
            self.options['expiration']
        )


class MTurk(object):
    def __init__(self, app=None):
        self.host = 'https://mechanicalturk.sandbox.amazonaws.com'
        self.secret_key = None
        self.access_id = None
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('MTURK_SECRET_KEY', None)
        app.config.setdefault('MTURK_ACCESS_ID', None)
        app.config.setdefault('MTURK_SANDBOX', True)
        self.update_credentials(app.config['MTURK_ACCESS_ID'],
                                app.config['MTURK_SECRET_KEY'])
        self.is_sandbox = app.config['MTURK_SANDBOX']
        self.valid_login = self.verify_aws_login()

    def update_credentials(self, aws_access_key_id, aws_secret_access_key):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def verify_aws_login(self):
        if ((self.aws_secret_access_key is None) or (
            self.aws_access_key_id is None)):
            logging.warning('No AWS keys found in app configuration')
        else:
            host = 'mechanicalturk.amazonaws.com'
            params = dict(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                host=host)
            self.mtc = MTurkConnection(**params)
            try:
                self.mtc.get_account_balance()
            except MTurkRequestError as e:
                return dict(success=False, message=e.error_message)
            else:
                return True

    def connect_to_turk(self):
        if not self.valid_login:
            logging.warning(
                'Sorry, unable to connect to Amazon Mechanical Turk. Please check your credentials')
            return False
        if self.is_sandbox:
            host = 'mechanicalturk.sandbox.amazonaws.com'
        else:
            host = 'mechanicalturk.amazonaws.com'

        mturkparams = dict(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            host=host)
        self.mtc = MTurkConnection(**mturkparams)
        return True

    def get_account_balance(self):
        if not self.connect_to_turk():
            return dict(success=False, message='Could not connect to AWS')
        try:
            balance = self.mtc.get_account_balance()
        except MTurkRequestError as e:
            return dict(success=False, message=e.error_message)
        else:
            return balance

    def get_reviewable_hits(self):
        if not self.connect_to_turk():
            return dict(success=False, message='Could not connect to AWS')
        try:
            hits = self.mtc.get_all_hits()
        except MTurkRequestError as e:
            return dict(success=False, message=e.error_message)

        reviewable_hits = [hit for hit in hits if hit.HITStatus == "Reviewable"
                           or hit.HITStatus == "Reviewing"]

        hits_data = [MTurkHIT({
            'hitid': hit.HITId,
            'title': hit.Title,
            'status': hit.HITStatus,
            'max_assignments': hit.MaxAssignments,
            'number_assignments_completed': hit.NumberOfAssignmentsCompleted,
            'number_assignments_pending': hit.NumberOfAssignmentsPending,
            'number_assignments_available': hit.NumberOfAssignmentsAvailable,
            'creation_time': hit.CreationTime,
            'expiration': hit.Expiration
        }) for hit in reviewable_hits]

        return hits_data

    def get_all_hits(self):
        """ Get all HITs """
        if not self.connect_to_turk():
            return False
        try:
            hits = self.mtc.get_all_hits()
        except MTurkRequestError as e:
            return dict(success=False, message=e.error_message)
        hits_data = [MTurkHIT({
            'hitid': hit.HITId,
            'title': hit.Title,
            'status': hit.HITStatus,
            'max_assignments': hit.MaxAssignments,
            'number_assignments_completed': hit.NumberOfAssignmentsCompleted,
            'number_assignments_pending': hit.NumberOfAssignmentsPending,
            'number_assignments_available': hit.NumberOfAssignmentsAvailable,
            'creation_time': hit.CreationTime,
            'expiration': hit.Expiration,
        }) for hit in hits]
        return hits_data

    def get_active_hits(self):
        """ Get active HITs """
        if not self.connect_to_turk():
            return dict(success=False, message='Could not connect to AWS')
        # hits = self.mtc.search_hits()
        try:
            hits = self.mtc.get_all_hits()
        except MTurkRequestError as e:
            return dict(success=False, message=e.error_message)
        active_hits = [hit for hit in hits if not hit.expired]
        hits_data = [MTurkHIT({
            'hitid': hit.HITId,
            'title': hit.Title,
            'status': hit.HITStatus,
            'max_assignments': hit.MaxAssignments,
            'number_assignments_completed': hit.NumberOfAssignmentsCompleted,
            'number_assignments_pending': hit.NumberOfAssignmentsPending,
            'number_assignments_available': hit.NumberOfAssignmentsAvailable,
            'creation_time': hit.CreationTime,
            'expiration': hit.Expiration,
        }) for hit in active_hits]
        return hits_data

    def get_hit(self, hit_id, response_groups=None):
        if not self.connect_to_turk():
            return dict(success=False, message='Could not connect to AWS')
        try:
            hit = self.mtc.get_hit(hit_id, response_groups)[0]
        except MTurkRequestError as e:
            return False
        return hit

    def get_workers(self, assignment_status=None):
        """ Get workers """
        if not self.connect_to_turk():
            return dict(success=False, message='Could not connect to AWS')
        try:
            hits = self.mtc.search_hits(sort_direction='Descending',
                                        page_size=20)
        except MTurkRequestError as e:
            return False
        hit_ids = [hit.HITId for hit in hits]
        workers_nested = [
            self.mtc.get_assignments(
                hit_id,
                status=assignment_status,
                sort_by='SubmitTime',
                page_size=100
            ) for hit_id in hit_ids]

        workers = [val for subl in workers_nested for val in
                   subl]  # Flatten nested lists

        worker_data = [{
            'hitId': worker.HITId,
            'assignmentId': worker.AssignmentId,
            'workerId': worker.WorkerId,
            'submit_time': worker.SubmitTime,
            'accept_time': worker.AcceptTime,
            'status': worker.AssignmentStatus,
            'completion_code': worker.answers[0][0].fields[0]
        } for worker in workers]
        return worker_data

    def bonus_worker(self, assignment_id, amount, reason=""):
        """ Bonus worker """
        if not self.connect_to_turk():
            return dict(success=False, message='Could not connect to AWS')
        try:
            bonus = MTurkConnection.get_price_as_price(amount)
            assignment = self.mtc.get_assignment(assignment_id)[0]
            worker_id = assignment.WorkerId
            self.mtc.grant_bonus(worker_id, assignment_id, bonus, reason)
            return True
        except MTurkRequestError as e:
            return dict(success=False, message=e.error_message)

    def approve_worker(self, assignment_id, feedback=None):
        """ Approve worker """
        if not self.connect_to_turk():
            return dict(success=False, message='Could not connect to AWS')
        try:
            self.mtc.approve_assignment(assignment_id, feedback=feedback)
            return True
        except MTurkRequestError as e:
            return False

    def reject_worker(self, assignment_id):
        """ Reject worker """
        if not self.connect_to_turk():
            return dict(success=False, message='Could not connect to AWS')
        try:
            self.mtc.reject_assignment(assignment_id, feedback=None)
            return True
        except MTurkRequestError as e:
            return dict(success=False, message=e.error_message)

    def unreject_worker(self, assignment_id):
        """ Unreject worker """
        if not self.connect_to_turk():
            return dict(success=False, message='Could not connect to AWS')
        try:
            self.mtc.approve_rejected_assignment(assignment_id)
            return True
        except MTurkRequestError as e:
            return dict(success=False, message=e.error_message)

    def assign_qualification(self, qualification_type_id, worker_id, value=1,
                             send_notification=True):
        if not self.connect_to_turk():
            return dict(success=False, message='Could not connect to AWS')
        try:
            self.mtc.assign_qualification(qualification_type_id, worker_id,
                                          value, send_notification)
            return True
        except MTurkRequestError as e:
            return dict(success=False, message=e.error_message)

    def revoke_qualification(self, subject_id, qualification_type_id,
                             reason=None):
        if not self.connect_to_turk():
            return False
        try:
            self.mtc.revoke_qualification(subject_id, qualification_type_id,
                                          reason)
            return True
        except MTurkRequestError as e:
            return dict(success=False, message=e.error_message)

    def notify_worker(self, worker_id, subject, message_text):
        if not self.connect_to_turk():
            return False
        try:
            self.mtc.notify_workers(worker_id, subject, message_text)
            return True
        except MTurkRequestError as e:
            return dict(success=False, message=e.error_message)

    def list_workers_with_qualification(self, qualification_type_id):
        if not self.connect_to_turk():
            return False
        try:
            workers = self.mtc.get_all_qualifications_for_qual_type(
                qualification_type_id)
        except MTurkRequestError as e:
            return dict(success=False, message=e.error_message)
        workers = [w.SubjectId for w in workers]
        return workers
