from flask_restful import Resource, reqparse
from services.game_service import GameService
from extension import db, cache
from sqlalchemy.exc import SQLAlchemyError
from models.player import Player


class GameResource(Resource):
    @cache.cached(timeout=600)
    def get(self, player_id):
        try:
            player = Player.query.get(player_id)
            if not player:
                return {"error": "Player not found"}, 404
            game = GameService(player_id)
            return game.get_player_status()
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500
        

    def patch(self, player_id):
        """Reset the game state for a player."""
        try:
            player = Player.query.filter_by(uuid=player_id).first()
            if not player:
                return {'message': 'Player not found'}, 404
            game = GameService(player_id)
            game.reset_game()
            db.session.commit()
            cache.delete(f'game_state_{player_id}')
            return {'message': 'Game state reset successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of an error
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500
            
    def post(self, player_id):
        """Save the game state for a player."""
        try:
            player = Player.query.filter_by(uuid=player_id).first()
            if not player:
                return {'message': 'Player not found'}, 404
            game = GameService(player_id)
            game.save_game_state()
            db.session.commit()
            cache.delete(f'game_state_{player_id}')
            return {'message': 'Game state saved successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback the transaction in case of an error
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500
