# import unittest
# from unittest.mock import patch, MagicMock
# from app import create_app, db
# from flask_restful import Api
# from models.player import Player
# from models.character import Character
# from models.map import Map
# from resources.player_resource import PlayerResource

# class PlayerResourceTestCase(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app()
#         self.client = self.app.test_client()
#         self.api = Api(self.app)
#         self.api.add_resource(PlayerResource, '/players', '/players/<string:player_id>')
#         self.app_context = self.app.app_context()
#         self.app_context.push()
#         db.create_all()

#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()

#     @patch('resources.player_resource.Player.query.get')
#     def test_get_player_by_id_valid(self, MockPlayerGet):
#         mock_player = MagicMock()
#         mock_player.to_dict.return_value = {'id': '123', 'name': 'Test Player'}
#         MockPlayerGet.return_value = mock_player

#         response = self.client.get('/players/123')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b'Test Player', response.data)

#     def test_get_player_by_id_invalid_uuid(self):
#         response = self.client.get('/players/invalid-uuid')
#         self.assertEqual(response.status_code, 400)
#         self.assertIn(b'Invalid UUID format', response.data)

#     @patch('resources.player_resource.Player.query.all')
#     def test_get_all_players(self, MockQueryAll):
#         mock_player = MagicMock()
#         mock_player.to_dict.return_value = {'id': '123', 'name': 'Test Player'}
#         MockQueryAll.return_value = [mock_player]

#         response = self.client.get('/players')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b'Test Player', response.data)

#     @patch('resources.player_resource.Player.query.filter_by')
#     @patch('resources.player_resource.Character.query.filter_by')
#     @patch('resources.player_resource.Map.query.filter_by')
#     def test_post_new_player(self, MockMapFilterBy, MockCharacterFilterBy, MockPlayerFilterBy):
#         MockCharacterFilterBy.return_value.first.return_value = MagicMock(uuid='char-uuid', inventory={})
#         MockMapFilterBy.return_value.first.return_value = MagicMock(uuid='map-uuid')
#         MockPlayerFilterBy.return_value.first.return_value = None

#         response = self.client.post('/players', json={'name': 'New Player', 'character_type': 'Adventurer'})
#         self.assertEqual(response.status_code, 201)
#         self.assertIn(b'New Player', response.data)

#     @patch('resources.player_resource.Player.query.get')
#     @patch('resources.player_resource.Character.query.filter_by')
#     def test_patch_player(self, MockCharacterFilterBy, MockPlayerGet):
#         mock_player = MagicMock(uuid='123', to_dict=lambda: {'id': '123', 'name': 'Updated Player'})
#         MockPlayerGet.return_value = mock_player
#         MockCharacterFilterBy.return_value.first.return_value = MagicMock(uuid='char-uuid')

#         response = self.client.patch('/players/123', json={'name': 'Updated Player', 'character_type': 'Hunter'})
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b'Updated Player', response.data)

#     def test_delete_player(self):
#         with patch('resources.player_resource.Player.query.get') as MockPlayerGet:
#             mock_player = MagicMock()
#             MockPlayerGet.return_value = mock_player

#             response = self.client.delete('/players/123')
#             self.assertEqual(response.status_code, 204)
#             self.assertIn(b'Player deleted successfully', response.data)

#     def test_post_player_character_not_found(self):
#         with patch('resources.player_resource.Character.query.filter_by') as MockCharacterFilterBy:
#             MockCharacterFilterBy.return_value.first.return_value = None

#             response = self.client.post('/players', json={'name': 'New Player', 'character_type': 'NonExistent'})
#             self.assertEqual(response.status_code, 404)
#             self.assertIn(b'Character not found', response.data)

#     def test_patch_player_character_not_found(self):
#         with patch('resources.player_resource.Player.query.get') as MockPlayerGet, \
#              patch('resources.player_resource.Character.query.filter_by') as MockCharacterFilterBy:
#             MockPlayerGet.return_value = MagicMock()
#             MockCharacterFilterBy.return_value.first.return_value = None

#             response = self.client.patch('/players/123', json={'character_type': 'NonExistent'})
#             self.assertEqual(response.status_code, 404)
#             self.assertIn(b'Character not found', response.data)

# if __name__ == '__main__':
#     unittest.main()
