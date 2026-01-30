import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import uuid
from resources.health_handler_resource import HealthResource

class TestHealthHandlerResource(unittest.TestCase):

    def setUp(self):
        self.health_handler = HealthResource()

    def test_validate_uuid_valid(self):
        valid_uuid = str(uuid.uuid4())
        self.assertTrue(self.health_handler.validate_uuid(valid_uuid))

    def test_validate_uuid_invalid(self):
        invalid_uuid = "not-a-uuid"
        self.assertFalse(self.health_handler.validate_uuid(invalid_uuid))

    def test_validate_uuid_empty_string(self):
        self.assertFalse(self.health_handler.validate_uuid(""))

    def test_validate_uuid_none(self):
        with self.assertRaises(TypeError):
            self.health_handler.validate_uuid(None)

    def test_validate_uuid_malformed(self):
        malformed_uuid = "12345678-1234-5678-1234-1234567890ab"  # Missing one character
        self.assertTrue(self.health_handler.validate_uuid(malformed_uuid))

if __name__ == '__main__':
    unittest.main()
