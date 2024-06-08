from scripts import *
import psycopg2


def create_db():
    query = create_db_script
    conn = psycopg2.connect(**settings)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    conn.close()


def create_tb_users():
    query = create_table_users
    conn = psycopg2.connect(**local_settings)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    conn.close()


def create_tb_messages():
    query = create_table_messages
    conn = psycopg2.connect(**local_settings)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    try:
        create_db()
    except psycopg2.Error as e:
        print(e)
    try:
        create_tb_users()
    except psycopg2.Error as e:
        print(e)
    try:
        create_tb_messages()
    except psycopg2.Error as e:
        print(e)
