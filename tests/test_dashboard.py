def test_dashboard_redirect(user, test_client):
    response = test_client.get('/')
    assert response.status_code == 302
