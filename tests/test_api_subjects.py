RESOURCE = '/api/v1/subjects/'

post_data = {
    'external_id': '931d8a79ec56394ed73d38e754390988',
    'assignment_id': 'debugSIP7SD',
    'assignment_name': 'test assignment',
    'worker_id': 'debugT7MSZ2',
    'hit_id': 'debugVY4J2G',
    'experiment_group': 'test',
}


def post_data_copy():
    data = dict()
    data.update(post_data)
    return data


def test_api_subject_post_successful(test_client):
    subject = post_data_copy()
    response = test_client.post_json(RESOURCE, subject)
    assert response.status_code == 201


def test_api_subject_post_validation_assignment_id_missing(test_client):
    subject = post_data_copy()
    del subject['assignment_id']
    response = test_client.post_json(RESOURCE, subject, expect_errors=True)

    assert response.status_code == 400

    response = response.json

    assert response['errors'][
               'assignment_id'] == "'assignment_id' is a required property"


def test_api_subject_post_validation_worker_id_missing(test_client):
    subject = post_data_copy()
    del subject['worker_id']
    response = test_client.post_json(RESOURCE, subject, expect_errors=True)

    assert response.status_code == 400

    response = response.json

    assert response['errors'][
               'worker_id'] == "'worker_id' is a required property"


def test_api_subject_post_validation_external_id_missing(test_client):
    subject = post_data_copy()
    del subject['external_id']
    response = test_client.post_json(RESOURCE, subject, expect_errors=True)

    assert response.status_code == 400

    response = response.json

    assert response['errors'][
               'external_id'] == "'external_id' is a required property"


def test_api_subject_post_validation_experiment_group_missing(test_client):
    subject = post_data_copy()
    del subject['experiment_group']
    response = test_client.post_json(RESOURCE, subject, expect_errors=True)

    assert response.status_code == 400

    response = response.json

    assert response['errors'][
               'experiment_group'] == "'experiment_group' is a required property"


def test_api_subject_post_validation_hit_id_missing(test_client):
    subject = post_data_copy()
    del subject['hit_id']
    response = test_client.post_json(RESOURCE, subject, expect_errors=True)

    assert response.status_code == 400

    response = response.json

    assert response['errors']['hit_id'] == "'hit_id' is a required property"


def test_api_subject_post_validation_experiment_group_missing(test_client):
    subject = post_data_copy()
    del subject['assignment_name']
    response = test_client.post_json(RESOURCE, subject, expect_errors=True)

    assert response.status_code == 400

    response = response.json

    assert response['errors'][
               'assignment_name'] == "'assignment_name' is a required property"


def test_api_subjects_get_all_successful(test_client):
    response = test_client.get(RESOURCE)
    assert response.status_code == 200
    response = response.json
    assert len(response) > 0


def test_api_subjects_get_one_successfull(test_client):
    response = test_client.get(RESOURCE + '1')
    assert response.status_code == 200


def test_api_subjects_put_successful(test_client):
    data = {
        "worker_id": "debug231G32"
    }
    response = test_client.put_json(RESOURCE + '1', params=data)
    assert response.status_code == 204
    response = test_client.get(RESOURCE + '1')
    response = response.json
    assert response['worker_id'] == 'debug231G32'
