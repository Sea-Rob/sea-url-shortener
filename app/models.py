from app.extensions import db
from datetime import datetime, timezone

class UrlMap(db.Model):
    __tablename__ = 'url_map'
    id = db.Column(db.Integer, primary_key=True)
    short_id = db.Column(db.String(5), unique=True, index=True, nullable=False)
    original_url = db.Column(db.String(2048), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class VisitMetric(db.Model):
    __tablename__ = 'visit_metric'
    id = db.Column(db.Integer, primary_key=True)
    url_id = db.Column(db.Integer, db.ForeignKey('url_map.id'), nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    referer = db.Column(db.String(2048))
    accessed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
