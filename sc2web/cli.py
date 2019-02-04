import os

from alembic.command import (
    branches as alembic_branch,
    current as alembic_current,
    downgrade as alembic_downgrade,
    history as alembic_history,
    revision as alembic_revision,
    upgrade as alembic_upgrade,
)
from flask.ext.script import Manager, prompt_bool

from .db import get_alembic_config, get_engine
from .web.app import app

__all__ = 'main',


@Manager
def manager(config=None):
    config = os.path.abspath(config)
    app.config.from_pyfile(config)
    assert 'DATABASE_URL' in app.config, 'DATABASE_URL missing in config.'
    return app


@manager.option('--message', '-m', dest='message', default=None)
def revision(message):
    """Add a revision"""
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    m = "--autogenerate"
    alembic_revision(config,
                     message=message,
                     autogenerate=prompt_bool(m, default=True))


@manager.option('--revision', '-r', dest='revision', default='head')
def upgrade(revision):
    """Upgrade a revision to --revision or newest revision"""
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    alembic_upgrade(config, revision)


@manager.option('--revision', '-r', dest='revision')
def downgrade(revision):
    """Downgrade a revision to --revision"""
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    alembic_downgrade(config, revision)


@manager.command
def history():
    """List of revision history."""
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    return alembic_history(config)


@manager.command
def branches():
    """Show current un-spliced branch point."""
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    return alembic_branch(config)


@manager.command
def current():
    """Current revision."""
    engine = get_engine()
    config, _ = get_alembic_config(engine)
    return alembic_current(config)


manager.add_option('-c', '--config', dest='config', required=True)


def main():
    manager.run()
