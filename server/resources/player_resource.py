from flask_restful import Resource, reqparse
from models.player import Player
from extension import db, cache
from models.character import Character
from models.map import Map
from sqlalchemy.exc import SQLAlchemyError
from config import Config
import uuid

class PlayerResource(Resource):
    def validate_uuid(self, uuid_string):
        """Helper function to validate UUID format."""
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False

    @cache.cached(timeout=600, key_prefix='player_{0}')
    def get(self, player_id=None):
        """Fetch player details"""
        if player_id is None:
            return self.get_all()
        else:
            return self.get_by_id(player_id)

    def get_by_id(self, player_id):
        """Fetch player details"""
        if not self.validate_uuid(player_id):
            return {'message': 'Invalid UUID format'}, 400
        
        try:
            player = Player.query.get(player_id)
            if not player:
                return {'message': 'Player not found'}, 404
            return player.to_dict(), 200
        except SQLAlchemyError as e:
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500

    def get_all(self):
        """Fetch all players"""
        try:
            players = Player.query.all()
            return [player.to_dict() for player in players], 200
        except SQLAlchemyError as e:
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500

    def post(self):
        """Create a new player"""
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help="Player name cannot be blank")
        parser.add_argument('character_type', type=str, required=True, choices=['Adventurer', 'Hunter', 'Warden'],
                            help="Invalid character type")
        args = parser.parse_args()

        try:
            default_start_location_coordinates = getattr(Config, 'DEFAULT_START_LOCATION_COORDINATES', {"x": 0, "y": 0})

            # Ensure the character type exists
            character = Character.query.filter_by(character_type=args['character_type']).first()
            if not character:
                return {'message': 'Character not found'}, 404

            # Fetch the default starting location
            starting_location = Map.query.filter_by(coordinates=default_start_location_coordinates).first()
            if not starting_location:
                return {'message': f'Starting location {default_start_location_coordinates} not found'}, 404

            # Check if a player with the same name already exists
            existing_player = Player.query.filter_by(name=args['name']).first()
            if existing_player:
                return {'message': 'Player with this name already exists'}, 400

            new_player = Player(
                name=args['name'],
                character_id=character.uuid,  # Ensure using character_id here
                health=100,
                score=0,
                inventory=character.inventory,
                current_location_id=starting_location.uuid  # Ensure matching UUID type
            )

            db.session.add(new_player)
            db.session.commit()

            return new_player.to_dict(), 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500

    def patch(self, player_id):
        """Update player attributes (e.g., name, character_type)"""
        if not self.validate_uuid(player_id):
            return {'message': 'Invalid UUID format'}, 400
        
        try:
            player = Player.query.get(player_id)
            if not player:
                return {'message': 'Player not found'}, 404

            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str)
            parser.add_argument('character_type', type=str, choices=['Adventurer', 'Hunter', 'Warden'])
            args = parser.parse_args()

            if args['name']:
                if Player.query.filter_by(name=args['name']).first():
                    return {'message': 'Player with this name already exists'}, 400
                player.name = args['name']

            if args['character_type']:
                character = Character.query.filter_by(character_type=args['character_type']).first()
                if not character:
                    return {'message': 'Character not found'}, 404
                player.character_id = character.uuid  # Update to use UUID
                player.inventory = character.inventory

            db.session.commit()
            return player.to_dict(), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500

    def delete(self, player_id):
        """Soft-delete a player"""
        if not self.validate_uuid(player_id):
            return {'message': 'Invalid UUID format'}, 400
        
        try:
            player = Player.query.get(player_id)
            if not player:
                return {'message': 'Player not found'}, 404

            player.soft_delete()
            db.session.commit()

            cache.delete(f'player_{player_id}')
            return {'message': 'Player deleted successfully'}, 204
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500
