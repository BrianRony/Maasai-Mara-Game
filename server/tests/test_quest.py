import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from extension import db
from models.quest import Quest
from app import create_app

class TestQuestModel(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_quest_creation(self):
        quest = Quest(title="Test Quest", description="A test quest", outcomes={})
        db.session.add(quest)
        db.session.commit()
        self.assertIsNotNone(quest.uuid)
        self.assertEqual(quest.title, "Test Quest")
        self.assertEqual(quest.description, "A test quest")
        self.assertEqual(quest.outcomes, {})

    def test_quest_update(self):
        quest = Quest(title="Original Quest", description="Original description", outcomes={})
        db.session.add(quest)
        db.session.commit()

        quest.title = "Updated Quest"
        quest.description = "Updated description"
        quest.outcomes = {"new_outcome": "value"}
        db.session.commit()

        updated_quest = db.session.get(Quest, quest.uuid)
        self.assertEqual(updated_quest.title, "Updated Quest")
        self.assertEqual(updated_quest.description, "Updated description")
        self.assertEqual(updated_quest.outcomes, {"new_outcome": "value"})

    def test_quest_deletion(self):
        quest = Quest(title="Deletable Quest", description="To be deleted", outcomes={})
        db.session.add(quest)
        db.session.commit()

        db.session.delete(quest)
        db.session.commit()

        deleted_quest = db.session.get(Quest, quest.uuid)
        self.assertIsNone(deleted_quest)

    def test_quest_empty_fields(self):
        quest = Quest(title="", description="", outcomes={})
        db.session.add(quest)
        db.session.commit()
        self.assertIsNotNone(quest.uuid)
        self.assertEqual(quest.title, "")
        self.assertEqual(quest.description, "")
        self.assertEqual(quest.outcomes, {})

    def test_quest_long_text(self):
        long_title = "A" * 255
        long_description = "B" * 1000
        quest = Quest(title=long_title, description=long_description, outcomes={"long": "C" * 100})
        db.session.add(quest)
        db.session.commit()
        self.assertEqual(quest.title, long_title)
        self.assertEqual(quest.description, long_description)
        self.assertEqual(quest.outcomes, {"long": "C" * 100})

if __name__ == '__main__':
    unittest.main()
