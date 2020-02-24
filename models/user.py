import sqlite3
from db import db

class UserModel(db.Model):

    # For sqlAlchemy
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def findByUsername(cls, username):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "SELECT * from users where username = ?"
        result = cursor.execute(query, (username,))
        row = result.fetchone() # fetch first row. If not present, returns None
        if row:
            #user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        conn.close()
        return user

    @classmethod
    def findByUserId(cls, _id):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "SELECT * from users where id = ?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone() # fetch first row. If not present, returns None
        if row:
            #user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        conn.close()
        return user
