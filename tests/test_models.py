from app.models import UrlMap, VisitMetric, db
from app.utils import generate_short_id

def test_urlmap_creation(app):
    with app.app_context():
        short_id = generate_short_id()
        url = UrlMap(short_id=short_id, original_url="https://example.com")
        db.session.add(url)
        db.session.commit()
        
        saved = db.session.query(UrlMap).filter_by(short_id=short_id).first()
        assert saved is not None
        assert saved.original_url == "https://example.com"
        assert saved.created_at is not None

def test_visit_metric_creation(app):
    with app.app_context():
        url = UrlMap(short_id="abcde", original_url="https://example.com")
        db.session.add(url)
        db.session.commit()
        
        metric = VisitMetric(
            url_id=url.id,
            ip_address="127.0.0.1",
            user_agent="TestAgent",
            referer="https://google.com"
        )
        db.session.add(metric)
        db.session.commit()
        
        saved = db.session.query(VisitMetric).first()
        assert saved.ip_address == "127.0.0.1"
        assert saved.user_agent == "TestAgent"
        assert saved.accessed_at is not None
