from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


# pretending to be a user and making some requests. (system tests for your API endpoints)
class ItemTest(BaseTest):
    # how do we get the authorization header?
    # override the base test setUp method
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                # the auth_request returns the access token which is to say jwt (access token == jwt)
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                # we need to include this jwt in the authorization header of our request
                # that is going to get the item from the database from our API
                auth_token = json.loads(auth_request.data)['access_token']  # jwt got from the database
                # header = {'Authorization': 'JWT ' + auth_token}
                self.access_token = f"JWT {auth_token}"

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                # if we don't have authorization to find an item what happens -> 401 unauthorized
                # when we make a request to '/item/test' and we don't include the authorization header.
                resp = client.get('/item/test')

                self.assertEqual(resp.status_code, 401)  # 401: unauthorized

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers={'Authorization': self.access_token})

                self.assertEqual(resp.status_code, 404)  # 404: not found

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                resp = client.get('/item/test', headers={'Authorization': self.access_token})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual({'name': 'test', 'price': 19.99},
                                 json.loads(resp.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()
                # none of these other endpoints need an authorization header. Only get endpoint needs it.
                # so for delete method, no need authorization header.
                resp = client.delete('/item/test')

                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(resp.data))

    # if we want to create an item, we would once again do the same thing but now posting some data
    # to the endpoint.
    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                # we're going to send over the data that we need in order to create an item.
                resp = client.post('/item/test', data={'price': 17.99, 'store_id': 1})
                # this data is sent in form data
                self.assertEqual(resp.status_code, 201)  # 201: created
                self.assertDictEqual({'name': 'test', 'price': 17.99},
                                     json.loads(resp.data))

    def test_create_duplicate_item(self):  # post == create
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()

                resp = client.post('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 400)  # 400: bad request
                self.assertDictEqual({'message': "An item with name 'test' already exists."},
                                     json.loads(resp.data))

    def test_put_item(self):  # put == update
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.put('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertEqual(ItemModel.find_by_name('test').store_id, 1)
                self.assertDictEqual({'name': 'test', 'price': 17.99},
                                     json.loads(resp.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                # have an item model already created.
                ItemModel('test', 5.99, 1).save_to_db()
                self.assertEqual(ItemModel.find_by_name('test').price, 5.99)
                # updating the price
                resp = client.put('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual({'name': 'test', 'price': 17.99},
                                     json.loads(resp.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()

                resp = client.get('/items')

                self.assertDictEqual({'items': [{'name': 'test', 'price': 5.99}]},
                                     json.loads(resp.data))


