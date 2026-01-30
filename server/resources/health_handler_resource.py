from flask_restful import Resource, reqparse
from models.player import Player
from extension import db, cache
from sqlalchemy.exc import SQLAlchemyError
import uuid

class HealthResource(Resource):
    def __init__(self):
        """Initialize request parser for health adjustment."""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('adjust', type=str, default='increase', choices=['increase', 'decrease'], help='Adjustment type is required')
        self.reqparse.add_argument('amount', type=int, default=0, help='Amount to adjust')

    def validate_uuid(self, uuid_string):
        """Helper function to validate UUID format."""
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False

    def get_health(self, player_id):
        """Retrieve the player's current health (Internal Helper)."""
        if not self.validate_uuid(player_id):
            return {'message': 'Invalid UUID format'}, 400
        
        try:
            player = Player.query.filter_by(uuid=player_id).first()
            if not player:
                return {'message': 'Player not found'}, 404
            return {'health': player.health}, 200
        except SQLAlchemyError as e:
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500

    @cache.cached(timeout=600, key_prefix=lambda player_id: f'health_{player_id}')
    def get(self, player_id):
        """Retrieve the player's current health (API Endpoint)."""
        return self.get_health(player_id)

    def update_health(self, player_id, change):
        """
        Helper method to adjust health directly.
        change: Integer (positive to heal, negative to damage).
        """
        if not self.validate_uuid(player_id):
            raise ValueError('Invalid UUID format')

        try:
            player = Player.query.filter_by(uuid=player_id).first()
            if not player:
                raise ValueError('Player not found')

            # Calculate new health with clamping 0-100
            new_health = player.health + change
            player.health = max(0, min(100, new_health))

            db.session.commit()
            cache.delete(f'health_{player_id}')
            return player.health
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Database error: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {str(e)}")

    def put(self, player_id):
        """Adjust the player's health (increase or decrease) via API."""
        if not self.validate_uuid(player_id):
            return {'message': 'Invalid UUID format'}, 400
        
        try:
            args = self.reqparse.parse_args()
            player = Player.query.filter_by(uuid=player_id).first()
            if not player:
                return {'message': 'Player not found'}, 404

            adjust = args['adjust']
            amount = args['amount']
            
            # Convert API args to signed change
            change = amount if adjust == 'increase' else -amount
            
            # Reuse the helper logic manually or just duplicate it for simplicity/API specific handling
            # Duplicating small logic here to keep API response format consistent with existing code
            if adjust == 'increase':
                player.health = min(player.health + amount, 100)
            elif adjust == 'decrease':
                player.health = max(player.health - amount, 0)

            db.session.commit()
            cache.delete(f'health_{player_id}')
            return {'health': player.health}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500
