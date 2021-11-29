import functools

import yhttp
from pony.orm import Database, db_session

from .cli import DatabaseCLI
from . import orm


def dbsession(func):

    @functools.wraps(func)
    def outter(*a, **kw):

        @db_session
        def wrapper(*a, **kw):
            try:
                return func(*a, **kw)
            except yhttp.HTTPStatus as ex:
                if ex.keepheaders:
                    return ex

                raise ex

        result = wrapper(*a, **kw)
        if isinstance(result, yhttp.HTTPStatus):
            raise result

        return result

    return outter


def install(app, db=None, cliarguments=None, create_objects=False):
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

        orm.initialize(db, app.settings.db.url, create_objects=create_objects)

    @app.when
    def shutdown(app):
        orm.deinitialize(db)

    return dbsession
