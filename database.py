import psycopg2
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


class Databases():
    def __init__(self):
        self.db = psycopg2.connect(host='localhost', dbname=env('PSQL_NAME'),
                                   user=env('PSQL_ID'),
                                   password=env('PSQL_PW'),
                                   port=env('PSQL_PORT'))
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
