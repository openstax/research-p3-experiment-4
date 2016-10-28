def test_dashboard_login_required_redirect(test_client):
    response = test_client.get('/')
    assert response.status_code == 302
    response = response.follow()
    assert 'phillip.grimaldi@rice.edu' in response


def test_dashboard_login_successful_after_redirect(test_client):
    response = test_client.get('/')
    assert response.status_code == 302
    response = response.follow()
    form = response.form
    form['email'] = 'mike@mike.com'
    form['password'] = 'password'
    response = form.submit()
    assert response.status_code == 302
    response = response.follow()
    assert 'My super dashboard' in response
