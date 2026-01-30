import unittest
import sys
import os
import uuid
from flask import Flask
from flask_restful import Resource
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from resources.character_resource import CharacterResource
from extension import cache

class TestCharacterResource(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['CACHE_TYPE'] = 'simple'
        cache.init_app(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.resource = CharacterResource()

    def tearDown(self):
        self.app_context.pop()

    def test_character_resource_is_resource(self):
        self.assertIsInstance(self.resource, Resource)

    def test_character_resource_methods(self):
        expected_methods = ['get']
        for method in expected_methods:
            self.assertTrue(hasattr(self.resource, method))

    def test_character_resource_get_method(self):
        self.assertTrue(callable(self.resource.get))

    @patch('resources.character_resource.Character')
    def test_get_all_characters(self, mock_Character):
        mock_characters = [MagicMock(), MagicMock()]
        mock_Character.query.all.return_value = mock_characters
        
        result = self.resource.get()
        
        self.assertEqual(len(result), 2)
        mock_Character.query.all.assert_called_once()

    @patch('resources.character_resource.Character')
    def test_get_specific_character(self, mock_Character):
        mock_character = MagicMock()
        mock_Character.query.get.return_value = mock_character

        test_uuid = str(uuid.uuid4())

        result = self.resource.get(test_uuid)

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], mock_character.to_dict())
        self.assertEqual(result[1], 200)
        mock_Character.query.get.assert_called_once_with(test_uuid)

if __name__ == '__main__':
    unittest.main()
