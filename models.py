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

    def change_username(self, username):
        self.username = username

    def save(self):
        """
        Method for saving the user to the database, or updating the password.
        :return: save/update the user to the database
        """
        conn = psycopg2.connect(**local_settings)
        try:
            cur = conn.cursor()
            if self._id == -1:
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
        return user[0] if user else None

    @staticmethod
    def load_user_by_id(user_id):
        """
        The method loads a user from the database by the given user_id
        :param user_id: id of the user we want to load
        :return: user with given id
        """
        conn = psycopg2.connect(**local_settings)
        try:
            cur = conn.cursor()
            query = """SELECT * FROM users WHERE id = %s;"""
            cur.execute(query, (user_id,))
            user = cur.fetchall()
            return user
        except Exception as e:
            print(e)
        finally:
            conn.close()

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
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            conn.close()

    @staticmethod
    def login_validate(username, password):
        conn = psycopg2.connect(**local_settings)
        try:
            cur = conn.cursor()
            query = """SELECT password FROM users WHERE username = %s;"""
            cur.execute(query, (username,))
            result = cur.fetchone()[0]
            if result == password:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            conn.close()

    def list_messages(self):
        """
        The method gives us a list of all the messages to the chosen user
        :return: list of messages to the user
        """
        conn = psycopg2.connect(**local_settings)
        try:
            cur = conn.cursor()
            query = """SELECT from_id, creation_date, text FROM messages WHERE to_id = %s;"""
            cur.execute(query, (self._id,))
            messages = cur.fetchall()
            formated_messages = []
            for message in messages:
                from_id, creation_date, text = message
                x = User.load_user_by_id(from_id)
                from_id = x[0][1]
                formated_datetime = creation_date.strftime('%H:%M %d.%m.%Y')
                formated_messages.append((from_id, formated_datetime, text))
            if formated_messages:
                return formated_messages
            else:
                return None
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def send_message(self, to_user, text):
        """
        Method for sending a message to the chosen user
        :param to_user: id of the message receiver
        :param text: text of the message
        :return: send a message and save it to the database
        """
        message = Message(self._id, to_user, text)
        message.save()


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
        Method for saving the message to the database, or updating it.
        :return: save/update the user to the database
        """
        conn = psycopg2.connect(**local_settings)
        try:
            cur = conn.cursor()
            if self._id != -1:
                query = """UPDATE messages SET from_id = %s, to_id = %s, text = %s WHERE id = %s;"""
                cur.execute(query, (self.from_id, self.to_id, self.text, self._id))
            else:
                query = """INSERT INTO messages(from_id, to_id, text, creation_date)
                VALUES(%s, %s, %s, %s) returning id, creation_date;"""
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
