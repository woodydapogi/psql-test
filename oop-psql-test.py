#!/usr/bin/python3
#

try:
        import psycopg2 as pg

except ImportError as i_err:
        print(i_err)


class DB_Test:
    def __init__(self, database, username, password, host, port):
        self.dbase = {
            'database': database,
            'user': username,
            'password': password,
            'host': host,
            'port': port
        }

    def conn_db(self):
        with pg.connect(
            database = self.dbase['database'],
            user = self.dbase['user'],
            password = self.dbase['password'],
            host = self.dbase['host'],
            port = self.dbase['port']
        ) as conn:

            return conn

    def show_data(self, table):
        db_conn = self.conn_db()
        with db_conn.cursor() as cur:
            cur.execute(f'SELECT * FROM {table}')
            data = cur.fetchall()
            return data

        db_conn.commit()
        db_conn.close()

db_conn = DB_Test('test-db', 'postgres', 'password123', 'localhost', 5432)

db_data = db_conn.show_data('network_device')

for data in db_data:
    print(data)
