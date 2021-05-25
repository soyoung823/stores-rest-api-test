"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):
    # runs for each test case (one whole class)
    @classmethod
    def setUpClass(cls):
        # Make sure database exists # 'sqlite:///'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['DEBUG'] = False  # to make the setUpClass method pass.
        app.config['PROPAGATE_EXCEPTIONS'] = True
        print('server start')
        # we only have to initialize a data base once for our app for every test file as opposed to every test.
        with app.app_context():
            db.init_app(app)

    # runs for each test method (one test function)
    def setUp(self):
        # we have to create the tables on every test since we are deleting the tables after every test.
        with app.app_context():
            db.create_all()
        print('server up')
        # Get a test client
        # we are generating a new test client every time we call self.app
        # give us a new test client in every test as opposed to (~아니라) creating the test client.
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
