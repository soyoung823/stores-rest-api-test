from models.user import UserModel
from tests.base_test import BaseTest
import json  # jason library comes with python so that we can convert dictionaries to json to send our api.


class UserTest(BaseTest):
    # test that we can register a user.
    # this test is pretending to be a client (external user) of our API.
    def test_register_user(self):
        # make requests to our API test client.
        # now we are able to both use the client and the app context is initialized,
        # so we can save things to a database and retrieve things from a database.
        with self.app() as client:  # fire up our client
            # we can send a post request.
            # client.post('')
            # because our methods are all saving things to a database the register method
            # we also need app context to be initialized.
            # load up the app context which again loads up all the required data
            # and allows us to access the database.
            with self.app_context():
                # send a post request to our actual API
                # then that's received by our post method and by the user register and it's going to run through it.
                response = client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                # json.loads(): loads the json string converted to a python dictionary.
                # request.data gives a json object actually so it needs to be a dictionary to compare.
                self.assertDictEqual({'message': 'User created successfully.'}, json.loads(response.data))

    # test that we can log in. (authentication)
    def test_register_and_login(self):
        # create a user
        with self.app() as client:
            with self.app_context():
                # using client.post or create userModel and save it to the database.
                client.post('/register', data={'username': 'test', 'password': '1234'})  # request
                # /auth endpoint requires that we send data in a json format.
                auth_response = client.post('/auth',
                                            data=json.dumps({'username': 'test', 'password': '1234'}),
                                            headers={'Content-Type': 'application/json'})

                self.assertIn('access_token', json.loads(auth_response.data).keys())  # ['access_token']
                # when we authenticate, we get back an access token (jwt) and whenever our application
                # requires that we are logged in to access a particular endpoint,
                # we are going to have to send this token to the endpoint and
                # flask_jwt is going to do the verification for us.

    # test the failure case for our use of resource which is
    # when a user with a user name already exists.
    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                # create a userModel and save it to the database.
                client.post('/register', data={'username': 'test', 'password': '1234'})
                # saved the response into a variable response.
                response = client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 400)  # bad request
                self.assertDictEqual({'message': 'A user with that username already exists.'},
                                     json.loads(response.data))



