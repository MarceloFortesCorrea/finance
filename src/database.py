
# database.py

import psycopg2


class Database:
    def __init__(self, database_url):
        try:
            self.conn = psycopg2.connect(database_url, sslmode='require')
            self.cur = self.conn.cursor()
        except IndexError:
            return IndexError

    def check_user(self, email, password):
        self.cur.execute(
            "SELECT password FROM users Where email = %s", (email,))
        result = self.cur.fetchone()
        if result:
            db_password = result[0]
            if password == db_password:
                return True
            else:
                return False
        else:
            return False

    def close(self):
        self.conn.close()
