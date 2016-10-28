def test_successful_login(test_client):
    """Login successful!"""
    response = test_client.get('/login')
    form = response.form
    form['email'] = 'mike@mike.com'
    form['password'] = 'password'
    response = form.submit()
    assert response.status_code == 302


def test_unsuccessful_login(test_client):
    """Login unsuccessful"""
    response = test_client.get('/login')
    form = response.form
    form['email'] = 'mike@mike.com'
    form['password'] = 'pizza'
    response = form.submit()
    assert 'Invalid password' in response
