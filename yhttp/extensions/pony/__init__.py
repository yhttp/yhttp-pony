from pony.orm import Database, db_session as dbsession

from .cli import DatabaseCLI
from . import uri


__version__ = '0.1.0'


def setup(app, echo=True):
    app.cliarguments.append(DatabaseCLI)
    db = Database()
    app.__database__ = db
    return db


def configure(app):
    settings = app.settings
    db = app.__database__

    if 'db' not in settings:
        raise ValueError(
            'Please provide db.url configuration entry, for example: ' \
            'postgres://:@/dbname'
        )

    url = uri.parse(settings.db.url)
    db.bind(**url)
    db.generate_mapping(create_tables=True)

