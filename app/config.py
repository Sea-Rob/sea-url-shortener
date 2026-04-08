import os
import logging

# Initialize a logger dedicated to the configuration loader
logger = logging.getLogger(__name__)

def setup_logging():
    """Configures global logging for the application."""
    log_level_env = os.environ.get('LOG_LEVEL', 'INFO').upper()
    numeric_level = getattr(logging, log_level_env, logging.INFO)

    log_handlers = [logging.StreamHandler()]

    log_file_path = os.environ.get('LOG_FILE')
    if log_file_path:
        log_dir = os.path.dirname(os.path.abspath(log_file_path))
        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir, exist_ok=True)
            except Exception as e:
                print(f"ERROR: Could not create log directory {log_dir}: {e}")
                log_dir = None

        if log_dir and os.access(log_dir, os.W_OK):
            try:
                file_handler = logging.FileHandler(log_file_path)
                log_handlers.append(file_handler)
            except Exception as e:
                print(f"ERROR: Could not initialize log file at {log_file_path}: {e}")
        else:
            print(f"WARNING: Log path {log_file_path} is not writeable. Falling back to console logging only.")

    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s [%(levelname)s] in %(name)s: %(message)s',
        handlers=log_handlers
    )

# Perform early logging setup so that configuration logs are captured
setup_logging()

def get_env_debug(var_name, default=None):
    """Utility to read environment variables and log them at DEBUG level."""
    val = os.environ.get(var_name, default)
    logger.debug(f"Config: Read environment variable {var_name} = '{val}' (default: '{default}')")
    return val

class Config:
    """Base configuration class."""
    # General Flask
    FLASK_ENV = get_env_debug('FLASK_ENV', 'production')
    SECRET_KEY = get_env_debug('SECRET_KEY', 'fvix4aqBbc7J3DOrUGTuHVuzl76htVXEPkjpOP9dHd3Jx0MsHBrGEpeZmHM9wIyr')
    
    # Application Specific
    API_KEY = get_env_debug('API_KEY', 'fvix4aqBbc7J3DOrUGTuHVuzl76htVXEPkjpOP9dHd3Jx0MsHBrGEpeZmHM9wIyr')
    
    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Logging
    LOG_LEVEL = get_env_debug('LOG_LEVEL', 'DEBUG').upper()
    LOG_FILE = get_env_debug('LOG_FILE', 'flask.log')

class DevelopmentConfig(Config):
    """Development-specific configuration."""
    SQLALCHEMY_DATABASE_URI = get_env_debug('DATABASE_URI', 'sqlite:///dev.db')
    DEBUG = True

class TestingConfig(Config):
    """Testing-specific configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = get_env_debug('TEST_DATABASE_URI', 'sqlite:///:memory:')

class ProductionConfig(Config):
    """Production-specific configuration using MySQL."""
    DB_USER = get_env_debug('DB_USER', 'smartene_short')
    DB_PASSWORD = get_env_debug('DB_PASSWORD', 'b*1(-~(n[EtJ')
    DB_HOST = get_env_debug('DB_HOST', 'localhost:3306')
    DB_NAME = get_env_debug('DB_NAME', 'sea_shortener')
    
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://smartene_short_user:b*1(-~(n[EtJ@localhost:3306/smartene_short"

# Mapping of environment names to config objects
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

def get_config():
    """Helper to retrieve the correct config class based on FLASK_ENV."""
    env = os.environ.get('FLASK_ENV', 'production').lower()
    return config_by_name.get(env, ProductionConfig)
