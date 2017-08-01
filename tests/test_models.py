from digital_logic.experiment.models import UserSubject


def test_get_subject_by_mturk_id(db):
    mturk_worker_id = 'debug5FQYY0'
    subject = UserSubject.get_by_mturk_worker_id(mturk_worker_id)
    assert subject.external_id == 'b9733ca6b41fec7402e5b014a826b2ed'

