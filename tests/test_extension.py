import pytest
from bddrest import status, response
from pony.orm import db_session as dbsession, PrimaryKey, Required
from yhttp import json

from yhttp.ext.pony import install


def test_extension(app, Given, freshdb):
    app.settings.merge(f'''
      db:
        url: {freshdb}
    ''')
    db = install(app)

    class Foo(db.Entity):
        id = PrimaryKey(int, auto=True)
        title = Required(str)

    @dbsession
    def mockup():
        Foo(title='foo 1')
        Foo(title='foo 2')

    app.ready()
    mockup()

    @app.route()
    @json
    @dbsession
    def get(req):
        return {f.id: f.title for f in Foo.select()}

    with Given():
        assert status == 200
        assert response.json == {'1': 'foo 1', '2': 'foo 2'}

    app.shutdown()


def test_exceptions(app):
    db = install(app)  # noqa: F841

    if 'db' in app.settings:
        del app.settings['db']

    with pytest.raises(ValueError):
        app.ready()
