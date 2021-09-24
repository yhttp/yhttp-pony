from bddcli import Given, Application as CLIApplication, status, stderr, when
from yhttp import Application
from yhttp.ext.pony import install


app = Application()
app.settings.merge('''
db:
  url: postgres://postgres:postgres@localhost/foo
''')
db = install(app)


def test_applicationcli():
    cliapp = CLIApplication('example', 'tests.test_cli:app.climain')
    with Given(cliapp, 'db --help'):
        assert status == 0
        assert stderr == ''

        when('db drop')
        when('db create')
        assert status == 0
        assert stderr == ''

        when('db drop')
        assert status == 0
        assert stderr == ''
