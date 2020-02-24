import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
createTableQuery = "CREATE TABLE if not exists users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(createTableQuery)

createItemTableQuery = "CREATE TABLE if not exists items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(createItemTableQuery)

conn.commit()
conn.close()
