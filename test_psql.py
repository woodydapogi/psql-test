#!/usr/bin/python3
#

try:
        import psycopg2 as pg
        import psycopg2.extras as pgx
        import os
        import sys

except ImportError as i_err:
        print(i_err)

def db_conn(database, user, password, host, port):

        conn, cur = None, None

        try:
                conn = pg.connect(
                        database = database,
                        user = user,
                        password = password,
                        host = host,
                        port = port
                        )

                if conn:
                        print('Connected')

                else:
                        print('Bye.')


                cur = conn.cursor(cursor_factory=pgx.DictCursor)

                cur.execute('DROP TABLE IF EXISTS network_device')

                tb_script = '''CREATE TABLE IF NOT EXISTS network_device (
                                        id int PRIMARY KEY,
                                        dev_name VARCHAR(50) NOT NULL,
                                        ip_addr VARCHAR(50) NOT NULL,
                                        subnet VARCHAR(50) NOT NULL
                                        ) '''

                cur.execute(tb_script)


                net_data = 'INSERT INTO network_device(id, dev_name, ip_addr, subnet) VALUES (%s, %s, %s, %s)'

                data = [
                        (1, 'MainROuter', '192.168.1.1', '255.255.255.0'),
                        (2, 'MainSwitch', '192.168.1.2', '255.255.255.0'),
                        (3, 'BackupRouter', '192.168.1.3', '255.255.255.0')
                ]

                for d in data:
                        cur.execute(net_data, d)

                net_device_data = cur.execute('SELECT * FROM network_device')

                for n_data in cur.fetchall():
                        print(n_data)

                        print(n_data['dev_name'])

                update_script = "UPDATE network_device SET ip_addr = '192.168.1.254' WHERE dev_name = 'MainSwitch'"

                cur.execute(update_script)

                for data in cur.fetchall():
                        print(data)

                conn.commit()

        except Exception as error:
                print(error)

        finally:
                if cur is not None:
                        cur.close()

                if conn is not None:
                        conn.close()


db_passwd = os.environ.get('DB_PASSWORD')

db_conn('test-db', 'postgres', db_passwd,'localhost', 5432)
