from flask_restful import Resource
from models.character import Character
from extension import db, cache
from sqlalchemy.exc import SQLAlchemyError
import uuid

class CharacterResource(Resource):
    
    def validate_uuid(self, character_id):
        """Helper function to validate UUID format."""
        try:
            uuid.UUID(character_id)
            return True
        except ValueError:
            return False

    @cache.cached(timeout=600)
    def get(self, character_id=None):
        """Fetch character details by ID with caching, or all characters if ID is not provided."""
        if character_id is None:
            # Fetch all characters
            return self.get_all()
        else:
            # Fetch a specific character
            return self.get_by_id(character_id)

    def get_by_id(self, character_id):
        """Fetch character details by ID."""
        if not self.validate_uuid(character_id):
            return {'message': 'Invalid UUID format'}, 400

        try:
            character = Character.query.get(character_id)
            if not character:
                return {'message': 'Character not found'}, 404
            return character.to_dict(), 200
        except SQLAlchemyError as e:
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500

    def get_all(self):
        """Fetch all characters from the database with caching."""
        try:
            characters = Character.query.all()
            if not characters:
                return {'message': 'Characters not found'}, 404
            return [character.to_dict() for character in characters], 200
        except SQLAlchemyError as e:
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500

    def delete(self, character_id):
        """Delete a character"""
        if not self.validate_uuid(character_id):
            return {'message': 'Invalid UUID format'}, 400

        try:
            character = Character.query.get(character_id)
            if not character:
                return {'message': 'Character not found'}, 404

            # Soft delete the character if applicable
            character.soft_delete()
            db.session.commit()
            return {'message': 'Character deleted successfully'}, 200
        except SQLAlchemyError as e:
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500
