import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from extension import db
from models.map import Map
from app import create_app

class TestMapModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_map_creation(self):
        map_obj = Map(location_name="Test Map", description="A test map", coordinates={"x": 0, "y": 0})
        db.session.add(map_obj)
        db.session.commit()
        self.assertIsNotNone(map_obj.uuid)
        self.assertEqual(map_obj.location_name, "Test Map")
        self.assertEqual(map_obj.description, "A test map")

    def test_map_update(self):
        map_obj = Map(location_name="Initial Map", description="Initial description", coordinates={"x": 0, "y": 0})
        db.session.add(map_obj)
        db.session.commit()

        map_obj.location_name = "Updated Map"
        map_obj.description = "Updated description"
        db.session.commit()

        updated_map = db.session.get(Map, map_obj.uuid)
        self.assertEqual(updated_map.location_name, "Updated Map")
        self.assertEqual(updated_map.description, "Updated description")

    def test_map_deletion(self):
        map_obj = Map(location_name="Map to Delete", description="This map will be deleted", coordinates={"x": 0, "y": 0})
        db.session.add(map_obj)
        db.session.commit()

        db.session.delete(map_obj)
        db.session.commit()

        deleted_map = db.session.get(Map, map_obj.uuid)
        self.assertIsNone(deleted_map)

    def test_map_name_unique(self):
        map1 = Map(location_name="Unique Map", description="First map", coordinates={"x": 0, "y": 0})
        db.session.add(map1)
        db.session.commit()

        map2 = Map(location_name="Unique Map", description="Second map", coordinates={"x": 1, "y": 1})
        db.session.add(map2)
        with self.assertRaises(Exception):  # Assuming the database enforces uniqueness
            db.session.commit()

    def test_map_name_required(self):
        map_obj = Map(description="Map without name", coordinates={"x": 0, "y": 0})
        db.session.add(map_obj)
        with self.assertRaises(Exception):  # Assuming location_name is a required field
            db.session.commit()

if __name__ == '__main__':
    unittest.main()
