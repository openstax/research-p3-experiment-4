from digital_logic.experiment.models import UserSubject


def test_subject_has_assessment_qualification_success(db, monkeypatch):

    def mockreturn():
        return True

    worker_id = 'debug5FQYY0'
    subject = UserSubject.get_by_mturk_worker_id(worker_id)
    assert subject.external_id == 'b9733ca6b41fec7402e5b014a826b2ed'
    monkeypatch.setattr(subject, 'has_assessment_qualification', mockreturn)
    has_qual = subject.has_assessment_qualification()
    assert has_qual is True


def test_subject_has_assessment_qualification_fail(db, monkeypatch):
    def mockreturn():
        return False

    worker_id = 'debug5FQYY0'
    subject = UserSubject.get_by_mturk_worker_id(worker_id)
    assert subject.external_id == 'b9733ca6b41fec7402e5b014a826b2ed'
    monkeypatch.setattr(subject, 'has_assessment_qualification', mockreturn)
    has_qual = subject.has_assessment_qualification()
    assert has_qual is False
