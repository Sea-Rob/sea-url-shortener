import logging
from flask import Blueprint, request, jsonify, redirect, current_app
from sqlalchemy.exc import IntegrityError

from app.models import UrlMap, VisitMetric
from app.extensions import db, limiter
from app.utils import generate_short_id, is_valid_url

logger = logging.getLogger(__name__)
bp = Blueprint('routes', __name__)

@bp.route('/shorten', methods=['POST'])
def shorten():
    logger.info("New request to /shorten")
    api_key = current_app.config.get('API_KEY')
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or auth_header != f"Bearer {api_key}":
        logger.warning(f"Unauthorized access attempt to /shorten from {request.remote_addr}")
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data or 'url' not in data:
        logger.error("Missing 'url' parameter in /shorten request.")
        return jsonify({"error": "Missing url parameter"}), 400

    url = data['url']
    logger.debug(f"Input URL to shorten: {url}")
    
    if not is_valid_url(url):
        logger.error(f"Validation failed for URL: {url}")
        return jsonify({"error": "Invalid URL"}), 400
    
    logger.info(f"Generating short ID for URL: {url}")
    for attempt in range(1, 11): # retry limit
        short_id = generate_short_id()
        logger.debug(f"Attempt {attempt}: Generated short_id: {short_id}")
        try:
            url_map = UrlMap(short_id=short_id, original_url=url)
            db.session.add(url_map)
            db.session.commit()
            logger.info(f"Successfully shortened {url} -> {short_id}")
            return jsonify({"short_id": short_id}), 201
        except IntegrityError:
            db.session.rollback()
            logger.warning(f"Short ID collision detected for {short_id}. Retrying...")
            continue
            
    logger.critical("Final failure to generate unique short ID after 10 attempts.")
    return jsonify({"error": "Failed to generate short ID"}), 500

@bp.route('/<short_id>', methods=['GET'])
@limiter.limit("5 per 5 minutes")
def redirect_to_url(short_id):
    # if length of short_id is greater than 5 redirect to url_for shorten
    logger.info(f"Redirect request for short_id: {short_id}")
    url_map = UrlMap.query.filter_by(short_id=short_id).first()
    
    if not url_map:
        logger.warning(f"No original mapping found for short_id: {short_id}")
        return jsonify({"error": "Not Found"}), 404

    ip_add = request.headers.get('X-Forwarded-For', request.remote_addr)
    # Extract simple ip
    if ip_add and ',' in ip_add:
        ip_add = ip_add.split(',')[0].strip()
    
    logger.info(f"Logging metric for short_id: {short_id} (IP: {ip_add})")
    try:
        metric = VisitMetric(
            url_id=url_map.id,
            ip_address=ip_add,
            user_agent=request.user_agent.string,
            referer=request.referrer
        )
        db.session.add(metric)
        db.session.commit()
    except Exception as e:
        logger.error(f"Failed to save visit metric for {short_id}: {e}", exc_info=True)
        # We don't fail the redirect if metric logging fails

    logger.debug(f"Redirecting {short_id} -> {url_map.original_url}")
    return redirect(url_map.original_url, code=302)
