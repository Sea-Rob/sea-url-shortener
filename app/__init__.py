import logging
from flask import Flask, redirect, jsonify
from app.extensions import db, limiter
from app.config import get_config

# Logger will be configured when get_config/config is imported
logger = logging.getLogger(__name__)

# --- FLASK APP INITIALIZATION ---
def create_app():
    app = Flask(__name__)
    
    # Load configuration
    ActiveConfig = get_config()
    app.config.from_object(ActiveConfig)
    
    logger.info(f"--- Sea URL Shortener Global App Initialized ---")
    logger.info(f"Operating Environment: {app.config.get('FLASK_ENV', 'production')}")
    
    # --- EXTENSIONS ---
    db.init_app(app)
    limiter.init_app(app)

    # --- ROUTES & BLUEPRINTS ---
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    logger.info("Routes registered.")

    from app.cli import setup_cli
    app.cli.add_command(setup_cli)
    logger.info("CLI commands registered.")

    # Catch-all error handler for logging
    @app.errorhandler(500)
    def internal_server_error(e):
        logger.error(f"UNHANDLED EXCEPTION: {e}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500

    return app

# Initialize the global app object for non-factory usage patterns
app = create_app()
