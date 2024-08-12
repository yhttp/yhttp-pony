from easycli import SubCommand
from pony.orm import db_session

from . import orm


class CreateObjectsCommand(SubCommand):
    __command__ = 'create'
    __aliases__ = ['c']

    def __call__(self, args):
        app = args.application
        orm.initialize(app.db, app.settings.db.url, create_objects=True)
        self.report_objects(args)

    @db_session
    def report_objects(self, args):
        app = args.application
        result = app.db.execute('''
            SELECT relname, relkind
            FROM pg_class
            WHERE relname !~ '^(pg|sql)_' AND relkind != 'v';
        ''')
        print('Following objects has been created successfully:')
        for name, kind in result.fetchall():
            print(kind, name)


class DatabaseObjectsCommand(SubCommand):
    __command__ = 'objects'
    __aliases__ = ['obj', 'o']
    __arguments__ = [
        CreateObjectsCommand,
    ]
