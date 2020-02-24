import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser() # check what params are passed in the request
    parser.add_argument('price', # parse only price from request json
        type = float,
        required = True,
        help = "This field cannot be blank")

    # @jwt_required
    # def get(self, name):
    #     for item in items:
    #         if item['name'] == name:
    #             return item, 200
    #     return {'item': None}, 404

    @jwt_required() # to require authentication before calling get service
    def get(self, name):
        #item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.findByName(name)
        if item:
            return item.json(), 200
        else:
            return {"Error": "Item {} not found".format(name)}, 400

    def post(cls, name):
        # if next(filter(lambda x: x['name'] == name, items), None) is not None:
        #     return {'message': "item {} is already existing".format(name)}, 400
        item = ItemModel.findByName(name)
        if item:
            return {'message': "item {} is already existing".format(name)}, 400

        data = Item.parser.parse_args()
        #item = {'name': name, 'price': data['price']}
        item = ItemModel(name, data['price'])
        try:
            #ItemModel.addItem(item)
            item.addItem()
        except:
            return {"Error": "Error creating new item {}".format(name)}, 500
        #items.append(item)
        return item.json(), 201

    def delete(self, name):
        # global items # to use the global items variable defined at the top
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {'Message': "item {} deleted".format(name)}
        item = ItemModel.findByName(name)
        if item:
            # delete an existing item
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()
            deleteQuery = "DELETE from items where name = ?"
            cursor.execute(deleteQuery, (name,))
            conn.commit()
            conn.close()
            return {"Message": "Item {} deleted successfully".format(name)}, 200
        return {"Error": "Item {} does not exist".format(name)}, 400

    def put(self, name):
        data = Item.parser.parse_args()
        #item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.findByName(name)
        #updatedItem = {'name': name, 'price': data['price']}
        updatedItem = ItemModel(name, data['price'])
        if item:
            # item['name'] = name
            # item['price'] = data['price']
            try:
                updatedItem.updateItem()
                #ItemModel.updateItem(updatedItem)
            except:
                return {"Error": "Error updating item {}".format(name)}, 500
            #item.update(data)
            #return {"Message": "item {} updated successfully".format(name)}, 200

        else:
            #items.append(item)
            try:
                updatedItem.addItem()
                #ItemModel.addItem(updatedItem)
            except:
                return {"Error": "Error creating item {}".format(name)}, 500
            #return {'Message': "Item {} added successfully".format(name)}, 201
        return updatedItem.json(), 200

class ItemList(Resource):
    def get(self):
        #return {'items': items}, 200
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = "select * from items"
        try:
            result = cursor.execute(query)
            items = []
            for row in result:
                item = {'name': row[0], 'price': row[1]}
                items.append(item)
            return {'items': items}, 200
        except:
            return {"Error": "Error getting items"}, 500
