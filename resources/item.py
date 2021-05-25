from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id.")

    # one of our endpoints needs the user to be logged in.
    # whenever we want to call this function before we enter the function,
    # we're going to check whether an authorization header was included with the JWT that we get
    # when authenticate when we call the /auth endpoint.
    # before we retrieve an item we are going to need to have JWT in the authorization header.
    # jwt_required() to protect routes.
    # jwt_required() runs before the get method and it checks the authorization header.
    # if the authorization header is not there or it's not valid, it returns a 401 error and
    # a message saying you're not logged in.
    # if the authorization header is there, it's going to get the JWT from the authorization header
    # we're going to look at exactly how to include jwt here and
    # is going to verify that i's a valid JWT and then it's going to allow us to access this method
    # because we didn't include the authorization header, the response is 401
    @jwt_required()  # authorization header: so only get endpoint needs authorization header.
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}
