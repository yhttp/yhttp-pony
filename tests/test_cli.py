from bddcli import Given, Application as CLIApplication, status, stderr, \
    when, stdout
import easycli
from yhttp import Application
from yhttp.ext.pony import install


class Bar(easycli.SubCommand):
    __command__ = 'bar'

    def __call__(self, args):
        print('bar')


app = Application()
app.settings.merge('''
db:
  url: postgres://postgres:postgres@localhost/foo
''')
install(app, cliarguments=[Bar])


def test_applicationcli():
    cliapp = CLIApplication('example', 'tests.test_cli:app.climain')
    with Given(cliapp, 'db --help'):
        assert stderr == ''
        assert status == 0

        when('db drop')
        when('db create')
        assert status == 0
        assert stderr == ''

        when('db drop')
        assert status == 0
        assert stderr == ''

        # Custom Command line interface
        when('db bar')
        assert status == 0
        assert stderr == ''
        assert stdout == 'bar\n'
