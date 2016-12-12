RESOURCE = '/api/v1/textbook/'


def test_api_textbook_get_all_text(test_client):
    response = test_client.get(RESOURCE)
    assert response.status_code == 200


def test_api_textbook_get_one__section_successful(test_client):
    response = test_client.get(RESOURCE + 'preface')
    assert response.status_code == 200


def test_api_textbook_get_one_section_unsuccessful(test_client):
    response = test_client.get(RESOURCE + 'pizza', expect_errors=True)
    assert response.status_code == 404
