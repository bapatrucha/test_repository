import sqlite3
from db import db

class ItemModel(db.Model):

    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def findByName(cls, name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "SELECT * from items where name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        conn.close()
        if row:
            #return {'item': {'name': row[0], 'price': row[1]}}
            #return cls(row[0], row[1])
            return cls(*row)

    def addItem(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "INSERT INTO items values (?,?)"
        print("creating a new item {}".format(self.name))
        cursor.execute(query, (self.name,self.price,))
        conn.commit()
        conn.close()

    def updateItem(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        updateQuery = "UPDATE items set price = ? where name = ?"
        cursor.execute(updateQuery, (self.price, self.name,))
        conn.commit()
        conn.close()
