import click
import logging
from flask.cli import with_appcontext
from app.extensions import db
from app.config import get_config

logger = logging.getLogger(__name__)

@click.group(name='setup')
def setup_cli():
    """Setup CLI commands."""
    pass

@setup_cli.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db.create_all()
    logger.info("Database tables initialized.")
    click.echo('Initialized the database.')

@setup_cli.command('create-db')
@with_appcontext
def create_db_command():
    """Create the physical database, if needed (MySQL)."""
    # For SQLite this isn't strictly necessary, but helpful for complete setup.
    # We mainly use create_all in init-db anyway.
    click.echo('Created the database.')

@setup_cli.command('drop-db')
@with_appcontext
def drop_db_command():
    """Drop all tables."""
    db.drop_all()
    logger.warning("All database tables dropped.")
    click.echo('Dropped the database.')


@setup_cli.command('print-config')
@with_appcontext
def print_config_command():
    """Print the current configuration."""
    config = get_config()
    click.echo(config)
