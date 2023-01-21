from bddrest import status, response, when, given
from yhttp import json, statuses, statuscode

from yhttp.ext.pony import install
from yhttp.ext.pony.metadata import PrimaryKey, Required, validate, Optional


def phonevalidator(req, value, container, field):
    return ''.join(value.split('-'))


def test_metadata_validation(app, Given, freshdb):
    app.settings.merge(f'''
      db:
        url: {freshdb}
    ''')

    dbsession = install(app, create_objects=True)

    class Foo(app.db.Entity):
        id = PrimaryKey(int, auto=True)
        title = Required(str, minlength=3, maxlength=30)
        email = Required(str, maxlength=50, pattern=r'^\w+@\w+\.\w+$')
        phone = Required(str, example='+1-333-3434', callback=phonevalidator)
        age = Required(int, minimum=18, maximum=120)
        role = Optional(str, readonly=True, default='user',
                        sqldefault='user')

    app.ready()

    @app.route()
    @validate(
        'foo',
        whitelist=['title', 'phone', 'age', 'email', 'role'],
        exceptions=dict(readonly=statuses.forbidden()),
        default_exception=statuses.status(700, 'Lorem Ipsum'),
        fields=dict(
            title=dict(
                minlength=2
            )
        )
    )
    @json
    @statuscode(statuses.created)
    @dbsession
    def create(req):
        foo = Foo(**req.form)
        return foo.to_dict()

    with Given(verb='CREATE', form=dict(
            title='fo',
            phone='+1-222-1111',
            age=22,
            email='w@a.com'
    )):
        assert status == 201
        assert response.json == {
            'id': 1,
            'age': 22,
            'email': 'w@a.com',
            'phone': '+12221111',
            'title': 'fo',
            'role': 'user'
        }

        when(form=given | dict(title='f'))
        assert status == 400

        when(form=given + dict(role='admin'))
        assert status == 403

    app.shutdown()
