import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from flask import Flask

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from resources.game_state_resource import GameResource
from models.player import Player
from services.game_service import GameService
from extension import cache

class TestGameResource(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['CACHE_TYPE'] = 'simple'
        cache.init_app(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.resource = GameResource()

    def tearDown(self):
        self.app_context.pop()

    @patch('resources.game_state_resource.Player')
    @patch('resources.game_state_resource.GameService')
    def test_get_existing_player(self, mock_GameService, mock_Player):
        mock_player = MagicMock()
        mock_Player.query.get.return_value = mock_player
        mock_game_service = MagicMock()
        mock_GameService.return_value = mock_game_service
        mock_game_service.get_player_status.return_value = {"status": "active"}

        result = self.resource.get("test_player_id")

        mock_Player.query.get.assert_called_once_with("test_player_id")
        mock_GameService.assert_called_once_with("test_player_id")
        mock_game_service.get_player_status.assert_called_once()
        self.assertEqual(result, {"status": "active"})

    @patch('resources.game_state_resource.Player')
    def test_get_non_existing_player(self, mock_Player):
        mock_Player.query.get.return_value = None

        result = self.resource.get("non_existing_player_id")

        mock_Player.query.get.assert_called_once_with("non_existing_player_id")
        self.assertEqual(result, ({"error": "Player not found"}, 404))

    @patch('resources.game_state_resource.Player')
    @patch('resources.game_state_resource.GameService')
    def test_get_with_exception(self, mock_GameService, mock_Player):
        mock_player = MagicMock()
        mock_Player.query.get.return_value = mock_player
        mock_GameService.side_effect = Exception("Test exception")

        result = self.resource.get("test_player_id")

        mock_Player.query.get.assert_called_once_with("test_player_id")
        mock_GameService.assert_called_once_with("test_player_id")
        self.assertEqual(result, ({'message': 'An unexpected error occurred', 'error': 'Test exception'}, 500))

if __name__ == '__main__':
    unittest.main()
