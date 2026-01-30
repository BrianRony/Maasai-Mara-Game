import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from extension import db
from models.character import Character
from app import create_app

class TestCharacterModel(unittest.TestCase):

    def setUp(self):
        # Create an app without passing any arguments
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        # Create all tables before each test
        db.create_all()


    def tearDown(self):
        # Clean up the database after each test
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_character_description_nullable(self):
        # Create a character without a description
        character = Character(character_type="Warrior", abilities="Combat")
        db.session.add(character)
        db.session.commit()
        # Assert that the description is None (nullable field)
        self.assertIsNone(character.description)

    def test_character_description_settable(self):
        # Create a character with a description
        description = "A brave adventurer"
        character = Character(character_type="Warrior", abilities="Combat", description=description)
        db.session.add(character)
        db.session.commit()
        # Assert that the description was set correctly
        self.assertEqual(character.description, description)

    def test_character_description_updateable(self):
        # Create a character with an initial description
        character = Character(character_type="Warrior", abilities="Combat", description="Initial description")
        db.session.add(character)
        db.session.commit()

        # Update the description
        new_description = "Updated description"
        character.description = new_description
        db.session.commit()

        # Fetch the updated character and assert the description was updated
        updated_character = db.session.get(Character, character.uuid)  # Use db.session.get instead of query.get
        self.assertEqual(updated_character.description, new_description)

    def test_character_description_empty_string(self):
        # Create a character with an empty description
        character = Character(character_type="Warrior", abilities="Combat", description="")
        db.session.add(character)
        db.session.commit()
        # Assert that the description is an empty string
        self.assertEqual(character.description, "")

    def test_character_description_long_text(self):
        # Create a character with a long description
        long_description = "A" * 1000  # Create a string of 1000 characters
        character = Character(character_type="Warrior", abilities="Combat", description=long_description)
        db.session.add(character)
        db.session.commit()
        # Assert that the long description was set correctly
        self.assertEqual(character.description, long_description)

if __name__ == '__main__':
    unittest.main()
