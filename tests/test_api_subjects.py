from utils import subject_data_copy

RESOURCE = '/api/v1/subjects/'


def test_api_subject_post_successful(test_client):
    subject = subject_data_copy()
    response = test_client.post_json(RESOURCE, subject)
    assert response.status_code == 201


# def test_api_subject_post_validation_assignment_id_missing(test_client):
#     subject = subject_data_copy()
#     del subject['assignment_id']
#     response = test_client.post_json(RESOURCE, subject, expect_errors=True)
#
#     assert response.status_code == 400
#
#     response = response.json
#
#     assert response['errors'][
#                'assignment_id'] == "'assignment_id' is a required property"


def test_api_subject_post_validation_worker_id_missing(test_client):
    subject = subject_data_copy()
    del subject['mturk_worker_id']
    response = test_client.post_json(RESOURCE, subject, expect_errors=True)

    assert response.status_code == 400

    response = response.json

    assert response['errors'][
               'mturk_worker_id'] == "'mturk_worker_id' is a required property"


def test_api_subject_post_validation_experiment_group_missing(test_client):
    subject = subject_data_copy()
    del subject['experiment_group']
    response = test_client.post_json(RESOURCE, subject, expect_errors=True)

    assert response.status_code == 400

    response = response.json

    assert response['errors'][
               'experiment_group'] == "'experiment_group' is a required property"


# def test_api_subject_post_validation_hit_id_missing(test_client):
#     subject = subject_data_copy()
#     del subject['hit_id']
#     response = test_client.post_json(RESOURCE, subject, expect_errors=True)
#
#     assert response.status_code == 400
#
#     response = response.json
#
#     assert response['errors']['hit_id'] == "'hit_id' is a required property"


# def test_api_subject_post_validation_experiment_group_missing(test_client):
#     subject = subject_data_copy()
#     del subject['assignment_id']
#     response = test_client.post_json(RESOURCE, subject, expect_errors=True)
#
#     assert response.status_code == 400
#
#     response = response.json
#
#     assert response['errors'][
#                'assignment_id'] == "'assignment_id' is a required property"


def test_api_subjects_get_all_successful(test_client):
    response = test_client.get(RESOURCE)
    assert response.status_code == 200
    response = response.json
    assert len(response) > 0


def test_api_subjects_get_one_successful(test_client):
    response = test_client.get(RESOURCE + '1')
    assert response.status_code == 200


def test_api_subjects_get_item_unsuccessful(test_client):
    response = test_client.get(RESOURCE + '2000', expect_errors=True)
    assert response.status_code == 404


def test_api_subjects_put_successful(test_client):
    data = {
        "experiment_group": "1"
    }
    response = test_client.put_json(RESOURCE + '1', params=data)
    assert response.status_code == 204
    response = test_client.get(RESOURCE + '1')
    response = response.json
    assert response['experiment_group'] == '1'
