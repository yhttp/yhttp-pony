from bddcli import Given, Application as CLIApplication, status, stderr, \
    stdout, when
from yhttp import Application
from yhttp.extensions.pony import setup as setuporm, configure as configureorm


app = Application()
app.settings.merge('''
db:
  url: postgres://postgres:postgres@localhost/foo
''')
db = setuporm(app)


def test_applicationcli():
    cliapp = CLIApplication('example', 'tests.test_cli:app.climain')
    #configureorm(app)
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
