RESOURCE = '/api/v1/exercises/'


def test_api_exercises_get_one_successful(test_client):
    response = test_client.get(RESOURCE + '1')
    assert response.status_code == 200


def test_api_exercises_get_one_unsuccessful(test_client):
    response = test_client.get(RESOURCE + '1000', expect_errors=True)
    assert response.status_code == 404
