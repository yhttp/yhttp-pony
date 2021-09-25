from pony.orm import Database

from .cli import DatabaseCLI
from . import orm


def install(app, db=None, cliarguments=None):
    app.cliarguments.append(DatabaseCLI)
    if cliarguments:
        DatabaseCLI.__arguments__.extend(cliarguments)

    if db is None:
        db = Database()

    app.db = db

    @app.when
    def ready(app):
        if 'db' not in app.settings:
            raise ValueError(
                'Please provide db.url configuration entry, for example: '
                'postgres://:@/dbname'
            )

        orm.initialize(db, app.settings.db.url)

    @app.when
    def shutdown(app):
        orm.deinitialize(db)

    return db
