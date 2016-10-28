def test_introduction_invalid_mturk_params(test_client):
    response = test_client.get('/exp/')
    assert response.status_code == 200
    assert 'Please accept the hit on Mechanical Turk' in response


def test_introduction_valid_mturk_params(test_client):
    params = dict(worker_id='debug7SDIPD',
                  assignment_id='debugSSDIP8',
                  hit_id='debug7SDPIS',
                  mode='debug')
    response = test_client.get('/exp/', params=params)
    assert response.status_code == 200
    assert 'Begin Experiment' in response


def test_start_no_mturk_params(test_client):
    response = test_client.get('/exp/start', expect_errors=True)
    assert response.status_code == 400
    assert 'Error: #1000' in response


def test_start_valid_mturk_params(test_client):
    params = dict(worker_id='debug7SDIPD',
                  assignment_id='debugSSDIP8',
                  hit_id='debug7SDPIS',
                  mode='test'
                  )
    headers = {'User-Agent': 'Py.Test'}
    response = test_client.get('/exp/start', params=params, headers=headers)
    assert 'Experiment Start!' in response


def test_start_debug_mode_disabled(test_client):
    params = dict(worker_id='debug7SDIPD',
                  assignment_id='debugSSDIP8',
                  hit_id='debug7SDPIS',
                  mode='test')
    headers = {'User-Agent': 'Py.Test'}
    response = test_client.get('/exp/start',
                               params=params,
                               headers=headers,
                               expect_errors=True)
    assert response.status_code == 400
    assert 'Error' in response


def test_start_debug_mode_enabled(test_client):
    params = dict(worker_id='debug7SDIPD',
                  assignment_id='debugSSDIP8',
                  hit_id='debug7SDPIS',
                  mode='debug')
    headers = {'User-Agent': 'Py.Test'}
    response = test_client.get('/exp/start',
                               params=params,
                               headers=headers,
                               expect_errors=True)
    assert response.status_code == 200
    assert 'Experiment Start!' in response
