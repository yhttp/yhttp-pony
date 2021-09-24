import os
import functools

import bddrest
import pytest

from yhttp import Application
from yhttp.ext.pony import createdbmanager


@pytest.fixture
def app():
    return Application()


@pytest.fixture
def Given(app):
    return functools.partial(bddrest.Given, app)


@pytest.fixture
def freshdb(app):
    host = os.environ.get('YHTTPPONY_TEST_DBHOST', 'localhost')
    user = os.environ.get('YHTTPPONY_TEST_USER', 'postgres')
    password = os.environ.get('YHTTPPONY_TEST_PASSWORD', 'postgres')
    dbname = 'yhttpponytestdb'
    dbmanager = createdbmanager(host, 'postgres', user, password)
    dbmanager.create(dbname, dropifexists=True)
    freshurl = f'postgres://{user}:{password}@{host}/{dbname}'
    app.settings.merge(f'''
      db:
        url: {freshurl}
    ''')
    yield freshurl
    app.shutdown()
    dbmanager.dropifexists(dbname)
