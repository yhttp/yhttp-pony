from bddcli import Given, Application as CLIApplication, status, stderr, \
    when, stdout
import easycli
from pony.orm import PrimaryKey, Required
from yhttp import Application
from yhttp.ext.pony import install


class Bar(easycli.SubCommand):
    __command__ = 'bar'

    def __call__(self, args):
        print('bar')


app = Application()
app.settings.merge('''
db:
  url: postgres://:@/foo
''')
install(app, cliarguments=[Bar])


class Foo(app.db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)


def test_applicationcli():
    cliapp = CLIApplication('example', 'tests.test_cli:app.climain')
    with Given(cliapp, 'db'):
        assert stderr == ''
        assert status == 0

        when('db drop')
        when('db create')
        assert stderr == ''
        assert status == 0

        when('db drop')
        assert status == 0
        assert stderr == ''

        # Custom Command line interface
        when('db bar')
        assert status == 0
        assert stderr == ''
        assert stdout == 'bar\n'

        when('db c')
        assert status == 0
        assert stderr == ''
        assert stdout == '''Following objects has been created successfully:
S foo_id_seq
r foo
i foo_pkey
'''
