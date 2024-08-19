import functools

from pony.orm import Database, db_session

import yhttp.core as y
from yhttp.ext.dbmanager import DatabaseCommand

from .cli import DatabaseObjectsCommand
from . import orm


def dbsession(func):

    @functools.wraps(func)
    def outter(*a, **kw):

        @db_session
        def wrapper(*a, **kw):
            try:
                return func(*a, **kw)
            except y.HTTPStatus as ex:
                if ex.keepheaders:
                    return ex

                raise ex

        result = wrapper(*a, **kw)
        if isinstance(result, y.HTTPStatus):
            raise result

        return result

    return outter


def install(app, db=None, cliarguments=None, create_objects=False):
    DatabaseCommand.__arguments__.append(DatabaseObjectsCommand)
    if cliarguments:
        DatabaseObjectsCommand.__arguments__.extend(cliarguments)

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
