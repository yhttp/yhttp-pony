import functools
import getpass

from easycli import SubCommand, Argument

from . import dbmanager, uri


getdbpass = functools.partial(getpass.getpass, 'Enter db password: ')


class DatabaseAdministrativeCommand(SubCommand):
    __arguments__ = [
        Argument('-H', '--host', default='localhost', help='DB hostname'),
        Argument('-d', '--database', default='postgres', help='DB name'),
        Argument('-u', '--user', default='postgres', help='DB username'),
        Argument(
            '-p', '--password',
            nargs='?',
            default='postgres',
            help='DB password'
        ),
    ]

    def getdbmanager(self, args):
        password = args.password or getdbpass()

        return dbmanager.PostgresqlManager(
            user=args.user,
            password=password,
            host=args.host,
            dbname=args.database
        )

    def getappdbinfo(self, args):
        dbsettings = args.application.settings.db
        url = uri.parse(dbsettings.url)
        return url


class CreateDatabase(DatabaseAdministrativeCommand):
    __command__ = 'create'
    __aliases__ = ['c']

    def __call__(self, args):
        info = self.getappdbinfo(args)
        self.getdbmanager(args) \
            .create(info['database'], owner=info.get('user'))


class DropDatabase(DatabaseAdministrativeCommand):
    __command__ = 'drop'
    __aliases__ = ['d']

    def __call__(self, args):
        info = self.getappdbinfo(args)
        self.getdbmanager(args).drop(info['database'])


class DatabaseCLI(SubCommand):
    __command__ = 'database'
    __aliases__ = ['db']
    __arguments__ = [
        CreateDatabase,
        DropDatabase
    ]
