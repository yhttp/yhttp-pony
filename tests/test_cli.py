from bddcli import Given, Application as CLIApplication, status, stderr, stdout
from yhttp import Application
from yhttp.extensions.pony import setup as setuporm, configure as configureorm


app = Application()
app.settings.merge('''
db:
  url: postgres://:@/yhttpponytest
''')
db = setuporm(app)


def test_applicationcli():
    cliapp = CLIApplication('example', 'tests.test_cli:app.climain')
    #configureorm(app)
    with Given(cliapp, 'db --help', working_directory='.'):
        print(stderr)
        assert status == 0

