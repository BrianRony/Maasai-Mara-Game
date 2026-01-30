import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restful import reqparse
from resources.inventory_handler_resource import InventoryResource

class TestInventoryResource(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.resource = InventoryResource()

    def tearDown(self):
        self.app_context.pop()

    def test_init_reqparse(self):
        self.assertIsInstance(self.resource.reqparse, reqparse.RequestParser)

    def test_reqparse_arguments(self):
        args = self.resource.reqparse.args
        self.assertEqual(len(args), 2)
        
        item_arg = next(arg for arg in args if arg.name == 'item')
        self.assertEqual(item_arg.type, str)
        self.assertTrue(item_arg.required)
        self.assertEqual(item_arg.help, 'Item is required')

        action_arg = next(arg for arg in args if arg.name == 'action')
        self.assertEqual(action_arg.type, str)
        self.assertEqual(action_arg.default, 'add')
        self.assertEqual(action_arg.choices, ['add', 'remove'])
        self.assertEqual(action_arg.help, 'Action can either be "add" or "remove".')

    @patch('resources.inventory_handler_resource.reqparse.RequestParser')
    def test_reqparse_add_argument_calls(self, mock_RequestParser):
        mock_parser = MagicMock()
        mock_RequestParser.return_value = mock_parser

        InventoryResource()

        mock_parser.add_argument.assert_any_call('item', type=str, required=True, help='Item is required')
        mock_parser.add_argument.assert_any_call('action', type=str, default='add', choices=['add', 'remove'], help='Action can either be "add" or "remove".')

if __name__ == '__main__':
    unittest.main()
