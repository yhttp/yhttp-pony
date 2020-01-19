import functools

import bddrest
import pytest

from yhttp import Application
from yhttp.extensions.pony import createdbmanager


@pytest.fixture
def app():
    return Application()


@pytest.fixture
def story():
    def given_(app, *a, **kw):
        return bddrest.Given(app, None, *a, **kw)

    return given_


@pytest.fixture
def when():
    return functools.partial(bddrest.when, None)



@pytest.fixture
def freshdb(app):
    host='localhost'
    user='postgres'
    password='postgres'
    dbname = 'yhttpponytestdb'
    dbmanager = createdbmanager(host, 'postgres', user, password)
    dbmanager.dropifexists(dbname)
    dbmanager.create(dbname)
    yield f'postgres://{user}:{password}@{host}/{dbname}'
    app.shutdown()
    dbmanager.dropifexists(dbname)
