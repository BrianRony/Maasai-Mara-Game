from flask_restful import Resource, reqparse
from models.quest import Quest
from extension import db, cache
from sqlalchemy.exc import SQLAlchemyError
import uuid

class QuestResource(Resource):
    def validate_uuid(self, uuid_string):
        """Helper function to validate UUID format."""
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False

    @cache.cached(timeout=600)
    def get(self, quest_id=None):
        """Retrieve quest details by ID or all quests"""
        if quest_id:
            return self.get_by_id(quest_id)
        else:
            return self.get_all()
        
    def get_by_id(self, quest_id):
        """Retrieve quest details by ID"""
        try:
            if not self.validate_uuid(quest_id):
                return {'message': 'Invalid UUID format'}, 400

            quest = Quest.query.get(quest_id)
            if not quest:
                return {'message': 'Quest not found'}, 404
            return quest.to_dict(), 200
        except SQLAlchemyError as e:
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500
        
    @cache.cached(timeout=600)
    def get_all(self):
        """Retrieve all quests"""
        try:
            quests = Quest.query.all()
            if not quests:
                return {'message': 'No quests found'}, 404
            return [quest.to_dict() for quest in quests], 200
        except SQLAlchemyError as e:
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500
        
    def post(self):
        """Create a new quest."""
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title is required')
        parser.add_argument('description', type=str, required=True, help='Description is required')
        parser.add_argument('outcomes', type=str, required=True, help='Outcomes are required')

        args = parser.parse_args()

        try:
            new_quest = Quest(
                title=args['title'],
                description=args['description'],
                outcomes=args['outcomes'],
                is_completed=False
            )

            db.session.add(new_quest)
            db.session.commit()
            return {'message': 'Quest created successfully', 'quest': new_quest.to_dict()}, 201
        
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of an error
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500

    
    def patch(self, quest_id):
        """Update quest details"""
        if not self.validate_uuid(quest_id):
            return {'message': 'Invalid UUID format'}, 400

        quest = Quest.query.get(quest_id)
        if not quest:
            return {'message': 'Quest not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('outcomes', type=str)
        parser.add_argument('is_completed', type=bool)

        args = parser.parse_args()

        try:
            if args['title'] is not None:
                quest.title = args['title']
            if args['description'] is not None:
                quest.description = args['description']
            if args['outcomes'] is not None:
                quest.outcomes = args['outcomes']
            if args['is_completed'] is not None:
                quest.is_completed = args['is_completed']

            db.session.commit()
            return {'message': 'Quest updated successfully', 'quest': quest.to_dict()}, 200
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of an error
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500
        
    def delete(self, quest_id):
        """Delete a quest"""
        if not self.validate_uuid(quest_id):
            return {'message': 'Invalid UUID format'}, 400

        quest = Quest.query.get(quest_id)
        if not quest:
            return {'message': 'Quest not found'}, 404

        try:
            # Perform soft deletion
            quest.soft_delete()
            db.session.commit()
            return {'message': 'Quest deleted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of an error
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500
