import abc

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DBManager(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create(self, name, owner):  # pragma: no cover
        pass

    @abc.abstractmethod
    def drop(self, name):  # pragma: no cover
        pass


class PostgresqlManager(DBManager):

    def __init__(self, host='localhost', dbname='postgres', user='postgres',
                 password='postgres'):
        self.connection = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password
        )
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    def execute(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
        finally:
            cursor.close()

    def create(self, name, owner=None, dropifexists=False):
        if dropifexists:
            self.dropifexists(name)

        query = f'CREATE DATABASE {name}' + \
            (f' WITH OWNER {owner}' if owner else '')

        self.execute(query)

    def drop(self, name):
        self.execute(f'DROP DATABASE {name}')

    def dropifexists(self, name):
        self.execute(f'DROP DATABASE IF EXISTS {name}')


def createdbmanager(*a, **k):
    return PostgresqlManager(*a, **k)
