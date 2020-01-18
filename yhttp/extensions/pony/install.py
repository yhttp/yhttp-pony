from pony.orm import Database

from .cli import DatabaseCLI
from . import uri


def install(app, db=None):
    app.cliarguments.append(DatabaseCLI)
    if db is None:
        db = Database()

    app.db = db

    @app.when
    def ready(app):
        settings = app.settings

        if 'db' not in settings:
            raise ValueError(
                'Please provide db.url configuration entry, for example: ' \
                'postgres://:@/dbname'
            )

        url = uri.parse(settings.db.url)
        db.bind(**url)
        db.generate_mapping(create_tables=True)

    return db
