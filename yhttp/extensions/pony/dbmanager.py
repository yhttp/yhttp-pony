import abc

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DBManager(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create(self, name, owner):
        pass

    @abc.abstractmethod
    def drop(self, name):
        pass


class PostgresqlManager(DBManager):

    def __init__(self, host, dbname, user, password):
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
            r = cursor.execute(query)
        finally:
            cursor.close()

    def create(self, name, owner=None):
        query = f'CREATE DATABASE {name}'
        if owner:
            query += f' WITH OWNER {owner}'

        self.execute(query)

    def drop(self, name):
        self.execute(f'DROP DATABASE {name}')


