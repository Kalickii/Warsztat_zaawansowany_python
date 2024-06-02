import psycopg2
from scripts import local_settings

class User:
    def __init__(self, username="", password="", _id=-1):
        self._id = _id
        self.username = username
        self.password = password

    def id(self):
        print(self._id)
        return self._id


    def change_password(self, password):
        self.password = password

    def save(self):
        conn = psycopg2.connect(**local_settings)
        try:
            cur = conn.cursor()
            if self._id == -1:
                existing_id = self.load_user_id_by_username(self.username)
                if existing_id:
                    self._id = existing_id
                    query1 = """UPDATE users SET username = %s, password = %s WHERE id = %s;"""
                    cur.execute(query1, (self.username, self.password, self._id))
                else:
                    query = """INSERT INTO users(username, password) VALUES(%s, %s) returning id;"""
                    cur.execute(query, (self.username, self.password))
                    new_id = cur.fetchone()[0]
                    self._id = new_id
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            conn.commit()
            conn.close()

    def load_user_id_by_username(self, username):
        conn = psycopg2.connect(**local_settings)
        try:
            cur = conn.cursor()
            query = """SELECT id FROM users WHERE username = %s;"""
            cur.execute(query, (username,))
            result = cur.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def load_user_by_username(self, username):
        conn = psycopg2.connect(**local_settings)
        cur = conn.cursor()
        query = """SELECT * FROM users WHERE username = %s;"""
        cur.execute(query, (username,))
        user = cur.fetchall()
        conn.close()
        print(user)

    def load_user_by_id(self, user_id):
        conn = psycopg2.connect(**local_settings)
        try:
            cur = conn.cursor()
            query = """SELECT * FROM users WHERE id = %s;"""
            cur.execute(query, (user_id,))
            user = cur.fetchall()
            conn.close()
            print(user)
        except Exception as e:
            print(e)


    def load_all_users(self):
        conn = psycopg2.connect(**local_settings)
        try:
            cur = conn.cursor()
            query = """SELECT * FROM users;"""
            cur.execute(query)
            users = cur.fetchall()
            print(users)
        except Exception as e:
            print(e)
        finally:
            conn.close()


    def delete(self):
        conn = psycopg2.connect(**local_settings)
        try:
            cur = conn.cursor()
            query = """DELETE FROM users WHERE id = %s;"""
            cur.execute(query, (self._id,))
            self._id = -1
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            conn.commit()
            conn.close()
