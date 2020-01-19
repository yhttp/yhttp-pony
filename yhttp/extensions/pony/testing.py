import pytest

from yhttp.extensions.pony import createdbmanager


@pytest.fixture
def freshdb(app):
    host='localhost'
    user='postgres'
    password='postgres'
    dbname = 'yhttpponytestdb'
    dbmanager = createdbmanager(host, 'postgres', user, password)
    dbmanager.create(dbname, dropifexists=True)
    yield f'postgres://{user}:{password}@{host}/{dbname}'
    app.shutdown()
    dbmanager.dropifexists(dbname)

