from tests.unit.unit_base_test import UnitBaseTest

from models.item import ItemModel


# from models.store import StoreModel
# from tests.base_test import BaseTest
# from app import app : we'll move it to a separate base test


class ItemTest(UnitBaseTest):
    def test_create_item(self):
        item = ItemModel('test', 19.99, 1)

        self.assertEqual(item.name, 'test',
                         "The name of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.price, 19.99,
                         "The price of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.store_id, 1,
                         "The store_id of the item after creation does not equal the constructor argument.")
        self.assertIsNone(item.store,
                          "The store of the item after creation is not None.")

    def test_item_json(self):
        item = ItemModel('test', 19.99, 1)
        expected = {
            'name': 'test',
            'price': 19.99
        }

        self.assertEqual(item.json(), expected,
                         "The JSON export of the item is incorrect. Received {}, expected {}.".format(item.json(),
                                                                                                      expected))
