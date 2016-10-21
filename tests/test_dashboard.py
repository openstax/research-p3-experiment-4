def test_dashboard_login_required_redirect(test_client):
    response = test_client.get('/')
    assert response.status_code == 302
