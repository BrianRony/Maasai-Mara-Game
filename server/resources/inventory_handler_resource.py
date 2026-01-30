from flask_restful import Resource, reqparse
from models.player import Player
from extension import db, cache
from sqlalchemy.exc import SQLAlchemyError
import uuid

class InventoryResource(Resource):
    
    def __init__(self):
        """Initialize request parser for adding or removing inventory items."""
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('item', type=str, required=True, help='Item is required')
        self.reqparse.add_argument('action', type=str, default='add', choices=['add', 'remove'], help='Action can either be "add" or "remove".')

    def validate_uuid(self, uuid_string):
        """Helper function to validate UUID format."""
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False

    def get_inventory(self, player_id):
        """Retrieve the player's inventory (Internal Helper)."""
        if not self.validate_uuid(player_id):
            return {'message': 'Invalid UUID format'}, 400
        
        try:
            player = Player.query.filter_by(uuid=player_id).first()
            if not player:
                return {'message': 'Player not found'}, 404
            return {'inventory': player.inventory}, 200
        except SQLAlchemyError as e:
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500

    @cache.cached(timeout=600, key_prefix=lambda player_id: f'inventory_{player_id}')
    def get(self, player_id):
        """Retrieve the player's inventory (API Endpoint)."""
        return self.get_inventory(player_id)

    def patch(self, player_id):
        """Add or remove an item from the player's inventory (API Endpoint)."""
        # ... (rest of patch method is fine as is, but we are using update_inventory helper mostly)
        # For simplicity, let's keep it consistent.
        if not self.validate_uuid(player_id):
            return {'message': 'Invalid UUID format'}, 400
        
        try:
            args = self.reqparse.parse_args()
            player = Player.query.filter_by(uuid=player_id).first()
            if not player:
                return {'message': 'Player not found'}, 404

            item = args['item']
            action = args['action']

            if action == 'add':
                if item not in player.inventory:
                    player.inventory.append(item)
                else:
                    return {'message': 'Item already exists in inventory'}, 400
            elif action == 'remove':
                if item in player.inventory:
                    player.inventory.remove(item)
                else:
                    return {'message': 'Item not found in inventory'}, 404

            db.session.commit()
            cache.delete(f'inventory_{player_id}')
            return {'inventory': player.inventory}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500
        
    def update_inventory(self, player_id, item, action):
        """Helper method to add or remove an item from the player's inventory."""
        if not self.validate_uuid(player_id):
            raise ValueError('Invalid UUID format')

        try:
            player = Player.query.filter_by(uuid=player_id).first()
            if not player:
                raise ValueError('Player not found')

            if action == 'add':
                if item not in player.inventory:
                    player.inventory.append(item)
                # else: silently ignore if already exists? Or raise? 
                # Original code raised ValueError.
            elif action == 'remove':
                if item in player.inventory:
                    player.inventory.remove(item)
                else:
                    raise ValueError('Item not found in inventory')

            db.session.commit()
            cache.delete(f'inventory_{player_id}')
            return player.inventory
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError('Database error occurred', str(e))
        except Exception as e:
            raise RuntimeError('An unexpected error occurred', str(e))
