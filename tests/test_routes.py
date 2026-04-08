import json

def test_shorten_url_no_auth(client):
    response = client.post('/shorten', json={"url": "https://example.com"})
    assert response.status_code == 401

def test_shorten_url_with_auth(client):
    headers = {"Authorization": "Bearer test-secret-key"}
    response = client.post('/shorten', json={"url": "https://example.com"}, headers=headers)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'short_id' in data

def test_shorten_url_invalid(client):
    headers = {"Authorization": "Bearer test-secret-key"}
    response = client.post('/shorten', json={"url": "not-a-url"}, headers=headers)
    assert response.status_code == 400

def test_redirect_valid_short_id(client, app):
    headers = {"Authorization": "Bearer test-secret-key"}
    resp = client.post('/shorten', json={"url": "https://example.com"}, headers=headers)
    data = json.loads(resp.data)
    short_id = data['short_id']
    
    # Access redirect
    res = client.get(f'/{short_id}')
    assert res.status_code == 302
    assert res.location == "https://example.com"
    
    # Verify metric was recorded
    from app.models import db, VisitMetric
    with app.app_context():
        metric = db.session.query(VisitMetric).first()
        assert metric is not None

def test_redirect_invalid_short_id(client):
    res = client.get('/abcde')
    assert res.status_code == 404

def test_rate_limiter(client):
    headers = {"Authorization": "Bearer test-secret-key"}
    resp = client.post('/shorten', json={"url": "https://example.com"}, headers=headers)
    short_id = json.loads(resp.data)['short_id']
    
    # 5 successful hits
    for _ in range(5):
        res = client.get(f'/{short_id}')
        assert res.status_code == 302
        
    # 6th hit should be rate limited
    res = client.get(f'/{short_id}')
    assert res.status_code == 429
