import sqlite3

conn = sqlite3.connect('data.db') # connect to db

cursor = conn.cursor() # cursor is responsible for executing the queries

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'Rucha', 'Rahul')
insert_query = "INSERT INTO users values (?,?,?)"
cursor.execute(insert_query, user)

users = [
    (2, 'Rahul', '1984'),
    (3, 'Aarya', '1991'),
    (4, 'Aai', 'ruchaaarya')
]

cursor.executemany(insert_query, users) # to insert multiple rows at a time

select_query = "SELECT * from users"
for row in cursor.execute(select_query):
    print(row)

conn.commit()
conn.close()
