import psycopg2
import datetime
from scripts import local_settings

now = datetime.datetime.now()
rounded_now = now.replace(second=0, microsecond=0)


class User:
    def __init__(self, username="", password="", _id=-1):
        self._id = _id
        self.username = username
        self.password = password


    @property
    def id(self):
        """returns the id of the user"""
        return self._id


    def change_password(self, password):
        self.password = password


    def save(self):
        """
        Method for saving the user to the database, or updating the password.
        :return: save/update the user to the database
        """
        conn = psycopg2.connect(**local_settings)
        try:
            cur = conn.cursor()
            if self._id == -1:
                existing_id = User.load_user_id_by_username(self.username)
                if existing_id:
                    self._id = existing_id
                    query = """UPDATE users SET username = %s, password = %s WHERE id = %s;"""
                    cur.execute(query, (self.username, self.password, self._id))
                else:
                    query = """INSERT INTO users(username, password) VALUES(%s, %s) returning id;"""
                    cur.execute(query, (self.username, self.password))
                    self._id = cur.fetchone()[0]
            else:
                query = """UPDATE users SET username = %s, password = %s WHERE id = %s;"""
                cur.execute(query, (self.username, self.password, self._id))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            conn.close()


    @staticmethod
    def load_user_id_by_username(username):
        """
        Method to check the id exists, used for save() method
        :return: id of the user if it exists, None otherwise
        """
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


    @staticmethod
    def load_user_by_username(username):
        """
        The method loads user from database by the given username.
        :return: user with given username
        """
        conn = psycopg2.connect(**local_settings)
        cur = conn.cursor()
        query = """SELECT * FROM users WHERE username = %s;"""
        cur.execute(query, (username,))
        user = cur.fetchall()
        conn.close()
        return user


    @staticmethod
    def load_user_by_id(user_id):
        """
        The method loads a user from the database by the given id
        :param user_id: id of the user we want to load
        :return: user with given id
        """
        conn = psycopg2.connect(**local_settings)
        try:
            cur = conn.cursor()
            query = """SELECT * FROM users WHERE id = %s;"""
            cur.execute(query, (user_id,))
            user = cur.fetchall()
            conn.close()
            return user
        except Exception as e:
            print(e)


    @staticmethod
    def load_all_users():
        """
        The method gives us a list of all the users in tuples in the database
        :return: list of all users
        """
        conn = psycopg2.connect(**local_settings)
        try:
            cur = conn.cursor()
            query = """SELECT * FROM users;"""
            cur.execute(query)
            users = cur.fetchall()
            return users
        except Exception as e:
            print(e)
        finally:
            conn.close()


    def delete(self):
        """
        Method for deleting a user from the database
        :return: deletes the user
        """
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



class Message:
    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self._creation_data = None


    @property
    def id(self):
        return self._id


    def save(self):
        """
        Method for saving the user to the database, or updating the password.
        :return: save/update the user to the database
        """
        conn = psycopg2.connect(**local_settings)
        try:
            cur = conn.cursor()
            if self._id != -1:
                query = """UPDATE messages SET from_id = %s, to_id = %s, text = %s WHERE id = %s;"""
                cur.execute(query, (self.from_id, self.to_id, self.text, self._id))
            else:
                query = """INSERT INTO messages(from_id, to_id, text) VALUES(%s, %s, %s) returning id, creation_date;"""
                cur.execute(query, (self.from_id, self.to_id, self.text, rounded_now))
                self._id, self._creation_data = cur.fetchone()
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            conn.close()


    @staticmethod
    def load_all_messages():
        """
        The method gives us a list of all the messages in tuples in the database
        :return: list of all messages
        """
        conn = psycopg2.connect(**local_settings)
        try:
            cur = conn.cursor()
            query = """SELECT * FROM messages;"""
            cur.execute(query)
            messages = cur.fetchall()
            return messages
        except Exception as e:
            print(e)
        finally:
            conn.close()

