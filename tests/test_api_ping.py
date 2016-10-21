def test_ping(test_client):
    response = test_client.get('/api/v1/ping/')
    assert response.json == {'message': 'pong'}
