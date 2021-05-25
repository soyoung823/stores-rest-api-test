from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('test', 'abcd')

        self.assertEqual(user.username, 'test', "The username isn't equal to 'test'.")
        self.assertEqual(user.password, 'abcd', "The user password isn't equal to 'abcd'.")