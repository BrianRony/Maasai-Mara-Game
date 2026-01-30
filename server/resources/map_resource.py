from flask_restful import Resource
from models.map import Map
from extension import db, cache
from sqlalchemy.exc import SQLAlchemyError
import uuid

class MapResource(Resource):

    def validate_uuid(self, uuid_string):
        """Helper function to validate UUID format."""
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False

    @cache.cached(timeout=600, key_prefix=lambda map_id=None: f'map_{map_id}' if map_id else 'all_maps')
    def get(self, map_id=None):
        """Fetch map details by ID with caching, or all map locations if ID is not provided."""
        if map_id is None:
            # Fetch all map locations
            return self.get_all()
        else:
            # Fetch a specific map location
            return self.get_by_id(map_id)

    def get_by_id(self, map_id):
        """Fetch map details by ID with caching."""
        if not self.validate_uuid(map_id):
            return {'message': 'Invalid UUID format'}, 400
        
        try:
            map_location = Map.query.get(map_id)
            if not map_location:
                return {'message': 'Map not found'}, 404
            return map_location.to_dict(), 200
        except SQLAlchemyError as e:
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500

    def get_all(self):
        """Fetch all map locations from the database."""
        try:
            maps = Map.query.all()
            if not maps:
                return {'message': 'Maps not found'}, 404
            return [map_location.to_dict() for map_location in maps], 200
        except SQLAlchemyError as e:
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500

    def delete(self, map_id):
        """Delete a map location."""
        if not self.validate_uuid(map_id):
            return {'message': 'Invalid UUID format'}, 400

        try:
            map_location = Map.query.get(map_id)
            if not map_location:
                return {'message': 'Map not found'}, 404

            # Perform the deletion
            db.session.delete(map_location)
            db.session.commit()
            
            # Invalidate the cache after deletion
            cache.delete(f'map_{map_id}')
            return {'message': 'Map deleted successfully'}, 200
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback in case of error
            return {'message': 'Database error occurred', 'error': str(e)}, 500
        except Exception as e:
            return {'message': 'An unexpected error occurred', 'error': str(e)}, 500
