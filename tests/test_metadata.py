import pytest
from bddrest import status, response
from yhttp import json

from yhttp.ext.pony import install
from yhttp.ext.pony.metadata import PrimaryKey, Required, get as getmetadata, \
    Metadata, getfield


def test_metadata(app, Given, freshdb):
    app.settings.merge(f'''
      db:
        url: {freshdb}
    ''')

    install(app, create_objects=True)

    class Foo(app.db.Entity):
        id = PrimaryKey(int, auto=True)
        title = Required(str, example='Alice')

    app.ready()

    @app.route()
    @json
    def get(req):
        return getmetadata('foo')

    with Given():
        assert status == 200
        assert response.json == {
            'name': 'foo',
            'fields': [{
                'callback': None,
                'default': None,
                'maximum': None,
                'maxlength': None,
                'minimum': None,
                'minlength': None,
                'name': 'id',
                'notnone': True,
                'pattern': None,
                'protected': False,
                'readonly': False,
                'required': False,
                'example': None,
                'type': 'int'
            }, {
                'callback': None,
                'default': None,
                'maximum': None,
                'maxlength': None,
                'minimum': None,
                'minlength': None,
                'name': 'title',
                'notnone': True,
                'pattern': None,
                'protected': False,
                'readonly': False,
                'required': True,
                'example': 'Alice',
                'type': 'str'
            }],
        }


def test_metadata_getfield(app, freshdb):
    app.settings.merge(f'''
      db:
        url: {freshdb}
    ''')

    install(app, create_objects=True)

    class Foo(app.db.Entity):
        id = PrimaryKey(int, auto=True)
        title = Required(str, example='Alice')

    app.ready()

    field = getfield('foo', 'title')
    assert field.todict() == {
        'callback': None,
        'default': None,
        'maximum': None,
        'maxlength': None,
        'minimum': None,
        'minlength': None,
        'name': 'title',
        'notnone': True,
        'pattern': None,
        'protected': False,
        'readonly': False,
        'required': True,
        'example': 'Alice',
        'type': 'str'
    }


def test_metadata_exceptions():

    with pytest.raises(NameError):
        Metadata(int, max_len=2)

    with pytest.raises(ValueError):
        Metadata(int, minlength=2)

    with pytest.raises(ValueError):
        Metadata(int, maxlength=2)
