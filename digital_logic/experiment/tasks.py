import datetime
from flask import current_app

from digital_logic.accounts.models import User


def check_for_start_assessment(user_id):
    from .service import get_latest_assignment_by_user_id
    from jobs import revoke_worker_qualification

    fail_reason = "Part II of HIT was not started within 1 hour."
    success_reason = "Part II of HIT was started within 1 hour, good luck!"
    mturk_qual = current_app.config['MTURK_PT2_QUALIFICATION']
    user = User.get(user_id)
    assignment = get_latest_assignment_by_user_id(user_id)

    if assignment and assignment.assignment_phase == 'Assessment':

        revoke_worker_qualification(user.mturk_worker_id,
                                    mturk_qual,
                                    reason=success_reason)
        return {'message': 'worker started assessment'}
    elif assignment and assignment.assignment_phase == 'Experiment':
        completed_time = [session.start_time
                          for session in assignment.sessions
                          if session.status == 'Completed'][0]
        diff = (datetime.datetime.utcnow() - completed_time).seconds

        if diff > 3600:
            revoke_worker_qualification(user.mturk_worker_id,
                                        mturk_qual,
                                        reason=fail_reason
                                        )

            return {'message': 'worker qualification revoked'}
        else:
            return {'message': 'worker has not started assessment %s seconds have elapsed' % diff}
    else:
        return {'message': 'Assessment or Experiment not found for this user'}


def approve_worker_assignments():
    from digital_logic.core import db, mturk
    from digital_logic.models import SubjectAssignment
    from digital_logic.experiment.feedback import FEEDBACK1, FEEDBACK2, DEFAULT

    def determine_feedback_msg(hit_id):
        hit = mturk.get_hit(hit_id)

        if 'Part 1' in hit.Title:
            return FEEDBACK1
        elif 'Part 2' in hit.Title:
            return FEEDBACK2
        else:
            return DEFAULT

    workers = mturk.get_workers('Submitted')

    if workers:

        for worker in workers:
            # Query gates_user_assignments table for a matching assignment_id
            assignment = db.session.query(SubjectAssignment).filter(
                SubjectAssignment.mturk_assignment_id == worker['assignmentId'],
                SubjectAssignment.mturk_completion_code != None).first()
            # Verify the completion code
            if assignment and assignment.mturk_completion_code == worker['completion_code']:
                feedback = determine_feedback_msg(worker['hitId'])

                approved = mturk.approve_worker(worker['assignmentId'],
                                                feedback=feedback)

                if approved:
                    return {'success': True, 'message': 'Worker %s was approved' % worker['workerId']}
                else:
                    return {'success': False, 'message': 'Worker %s was not approved' % worker['workerId'] }

            else:
                return {'success': False, 'message': 'No assignment found or completion code did not validate'}
    else:
        return {'success': False, 'message': 'No workers to approve'}
