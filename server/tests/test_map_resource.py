import unittest
from resources.map_resource import MapResource

class TestMapResource(unittest.TestCase):

    def setUp(self):
        self.map_resource = MapResource()

    def test_validate_uuid_valid(self):
        # Test with a valid UUID
        valid_uuid = "12345678-1234-5678-1234-567812345678"
        self.assertTrue(self.map_resource.validate_uuid(valid_uuid))

    def test_validate_uuid_invalid(self):
        # Test with an invalid UUID (non-UUID characters)
        invalid_uuid = "invalid-uuid-string"
        self.assertFalse(self.map_resource.validate_uuid(invalid_uuid))
