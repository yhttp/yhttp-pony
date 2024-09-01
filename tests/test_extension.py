import pytest
from bddrest import status, response, when
from pony.orm import PrimaryKey, Required
from yhttp.core import json, statuses

from yhttp.ext.pony import install, dbsession


def test_extension(app, Given, freshdb):
    freshdb = freshdb.replace('postgresql', 'postgres')

    app.settings.merge(f'''
      db:
        url: {freshdb}
    ''')

    install(app, create_objects=True)

    class Foo(app.db.Entity):
        id = PrimaryKey(int, auto=True)
        title = Required(str)

    app.ready()

    @dbsession
    def mockup():
        Foo(title='foo 1')
        Foo(title='foo 2')

    mockup()

    @app.route()
    @json
    @dbsession
    def get(req):
        return {f.id: f.title for f in Foo.select()}

    @app.route()
    @json
    @dbsession
    def got(req):
        Foo(title='foo')
        raise statuses.created()

    @app.route()
    @json
    @dbsession
    def err(req):
        Foo(title='qux')
        raise statuses.badrequest()

    @dbsession
    def getfoo(title):
        return Foo.get(title=title)

    with Given():
        assert status == 200
        assert response.json == {'1': 'foo 1', '2': 'foo 2'}

        when(verb='err')
        assert status == 400
        qux = getfoo('qux')
        assert qux is None

        when(verb='got')
        assert status == 201

        foo = getfoo('foo')
        assert foo is not None

    app.shutdown()


def test_exceptions(app):
    dbsession = install(app)  # noqa: F841

    if 'db' in app.settings:
        del app.settings['db']

    with pytest.raises(ValueError):
        app.ready()
