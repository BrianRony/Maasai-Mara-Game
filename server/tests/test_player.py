import unittest
from sqlalchemy.orm import relationship
from models.player import Player
from models.map import Map
from extension import db
from app import create_app

class TestPlayerModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_player_current_location_relationship(self):
        map_location = Map(location_name="Test Location", coordinates={"lat": 0, "lng": 0})
        db.session.add(map_location)
        db.session.commit()

        player = Player(name="Test Player", current_location=map_location)
        db.session.add(player)
        db.session.commit()

        self.assertEqual(player.current_location, map_location)
        self.assertIn(player, map_location.players)

    def test_player_current_location_nullable(self):
        player = Player(name="Test Player")
        db.session.add(player)
        db.session.commit()

        self.assertIsNone(player.current_location)

    def test_player_current_location_updateable(self):
        map_location1 = Map(location_name="Location 1", coordinates={"lat": 0, "lng": 0})
        map_location2 = Map(location_name="Location 2", coordinates={"lat": 1, "lng": 1})
        db.session.add_all([map_location1, map_location2])
        db.session.commit()

        player = Player(name="Test Player", current_location=map_location1)
        db.session.add(player)
        db.session.commit()

        player.current_location = map_location2
        db.session.commit()

        updated_player = db.session.get(Player, player.uuid)
        self.assertEqual(updated_player.current_location, map_location2)
        self.assertIn(player, map_location2.players)
        self.assertNotIn(player, map_location1.players)

    def test_player_current_location_cascade_delete(self):
        map_location = Map(location_name="Test Location", coordinates={"lat": 0, "lng": 0})
        db.session.add(map_location)
        db.session.commit()

        player = Player(name="Test Player", current_location=map_location)
        db.session.add(player)
        db.session.commit()

        db.session.delete(map_location)
        db.session.commit()

        updated_player = db.session.get(Player, player.uuid)
        self.assertIsNone(updated_player.current_location)

if __name__ == '__main__':
    unittest.main()
