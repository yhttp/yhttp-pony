from .cli import DatabaseCLI


__version__ = '0.1.0'


def setup(app):
    from pony.orm import Database
    app.cliarguments.append(DatabaseCLI)
    db = Database()
    app.db = db


def configure(app):
    from . import uri
    settings = app.settings
    db = app.db

    if 'db' not in settings:
        raise ValueError(
            'Please provide db.url configuration entry, for example: ' \
            'postgres://:@/dbname'
        )

    url = uri.parse(settings.db.url)
    db.bind(**url)
    db.generate_mapping(create_tables=True)

