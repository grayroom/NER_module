import psycopg2
import os


class Databases():
    def __init__(self):
        self.db = psycopg2.connect(host=os.environ['PSQL_HOST'], dbname=os.environ['PSQL_NAME'],
                                   user=os.environ['PSQL_ID'],
                                   password=os.environ['PSQL_PW'],
                                   port=os.environ['PSQL_PORT'])
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()
        self.cursor.close()

    def execute(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()
