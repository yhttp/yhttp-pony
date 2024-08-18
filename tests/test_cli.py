import os

from bddcli import Given, Application as CLIApplication, status, stderr, \
    when, stdout
import easycli
from pony.orm import PrimaryKey, Required

from yhttp.core import Application
from yhttp.ext import pony as ponyext, dbmanager
from yhttp.dev.fixtures import CICD


class Bar(easycli.SubCommand):
    __command__ = 'bar'

    def __call__(self, args):
        print('bar')


class Baz(easycli.SubCommand):
    __command__ = 'baz'

    def __call__(self, args):
        print('baz')


_host = os.environ.get('YHTTP_DB_DEFAULT_HOST', 'localhost' if CICD else '')
_user = os.environ.get('YHTTP_DB_DEFAULT_USER', 'postgres' if CICD else '')
_pass = os.environ.get('YHTTP_DB_DEFAULT_PASS', 'postgres' if CICD else '')


app = Application()
app.settings.merge(f'''
db:
  url: postgres://{_user}:{_pass}@{_host}/foo
''')
dbmanager.install(app, cliarguments=[Bar])
ponyext.install(app, cliarguments=[Baz])


class Foo(app.db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)


def test_applicationcli(cicd):
    env = os.environ.copy()
    if cicd:
        env.setdefault('YHTTP_DB_DEFAULT_HOST', 'localhost')
        env.setdefault('YHTTP_DB_DEFAULT_ADMINUSER', 'postgres')
        env.setdefault('YHTTP_DB_DEFAULT_ADMINPASS', 'postgres')

    cliapp = CLIApplication('example', 'tests.test_cli:app.climain')
    with Given(cliapp, 'db', environ=env):
        assert stderr == ''
        assert status == 0

        # Custom Command line interface
        when('db bar')
        assert status == 0
        assert stderr == ''
        assert stdout == 'bar\n'

        when('db objects baz')
        assert status == 0
        assert stderr == ''
        assert stdout == 'baz\n'

        when('db drop')
        when('db create')
        assert stderr == ''
        assert status == 0

        when('db objects create')
        assert status == 0
        assert stderr == ''
        assert stdout == '''Following objects has been created successfully:
S foo_id_seq
r foo
i foo_pkey
'''
