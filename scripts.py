
settings = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'coderslab',
    'dbname': 'postgres',
}

local_settings = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'coderslab',
    'dbname': 'workspace_2',
}

create_db_script = f"""CREATE DATABASE workspace_2;
"""
create_table_users = f"""CREATE TABLE users(id serial PRIMARY KEY , username varchar(255), password varchar(80));
"""
create_table_messages = f"""CREATE TABLE messages(
id serial PRIMARY KEY,
from_id int,
to_id int,
FOREIGN KEY(from_id) references users(id),
FOREIGN KEY(to_id) references users(id),
creation_date timestamp,
text varchar(255));
"""
