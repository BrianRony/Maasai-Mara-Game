from flask_restful import Resource, reqparse
from flask import request
from services.events_logic import MaasaiMaraEventsLogic
from models.player import Player
from extension import db

class SafariEventResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('player_id', type=str, required=True, help='Player ID is required')

class StartSafariResource(SafariEventResource):
    def post(self):
        args = self.reqparse.parse_args()
        game = MaasaiMaraEventsLogic(args['player_id'])
        return game.start_safari()

class ObserveWildlifeResource(SafariEventResource):
    def get(self):
        args = request.args
        player_id = args.get('player_id')
        if not player_id:
            return {'success': False, 'message': 'Player ID is required'}, 400
        
        try:
            game = MaasaiMaraEventsLogic(player_id)
            wildlife = game.get_observable_wildlife()
            player_stats = game.get_player_status()
            return {
                'success': True,
                'wildlife': wildlife,
                'player_stats': player_stats
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500

    def post(self):
        try:
            player_id = request.args.get('player_id') or request.json.get('player_id')
            if not player_id:
                return {'success': False, 'message': 'Player ID is required'}, 400

            game = MaasaiMaraEventsLogic(player_id)
            return game.observe_wildlife()
        except Exception as e:
            return {'success': False, 'message': str(e)}, 500


class InteractWithLocalsResource(SafariEventResource):
    def post(self):
        args = self.reqparse.parse_args()
        game = MaasaiMaraEventsLogic(args['player_id'])
        # Now returns standard dict
        return game.interact_with_locals()

class HandleWeatherChangeResource(SafariEventResource):
    def post(self):
        args = self.reqparse.parse_args()
        game = MaasaiMaraEventsLogic(args['player_id'])
        return game.handle_weather_change()

class TakePhotoResource(SafariEventResource):
    def post(self):
        args = self.reqparse.parse_args()
        game = MaasaiMaraEventsLogic(args['player_id'])
        return game.take_photo()

class FindItemResource(SafariEventResource):
    def post(self):
        args = self.reqparse.parse_args()
        game = MaasaiMaraEventsLogic(args['player_id'])
        return game.find_item()

class UseItemResource(SafariEventResource):
    def __init__(self):
        super().__init__()
        self.reqparse.add_argument('item_name', type=str, required=True, help='Item name is required')

    def post(self):
        args = self.reqparse.parse_args()
        game = MaasaiMaraEventsLogic(args['player_id'])
        return game.use_item(args['item_name'])

class CompleteSafariResource(SafariEventResource):
    def post(self):
        args = self.reqparse.parse_args()
        game = MaasaiMaraEventsLogic(args['player_id'])
        return game.complete_safari()
