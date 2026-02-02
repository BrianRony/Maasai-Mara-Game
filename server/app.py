import os
from flask import Flask
from flask_restful import Api
from config import Config
from test_config import TestingConfig
from flask_cors import CORS
from extension import db, migrate, cache
from resources.player_resource import PlayerResource
from resources.character_resource import CharacterResource
from resources.map_resource import MapResource
from resources.quest_resource import QuestResource
from resources.game_state_resource import GameResource
from resources.health_handler_resource import HealthResource
from resources.inventory_handler_resource import InventoryResource
from resources.safari_event_resource import (
    StartSafariResource, ObserveWildlifeResource, InteractWithLocalsResource,
    HandleWeatherChangeResource, TakePhotoResource, FindItemResource,
    UseItemResource, CompleteSafariResource
)

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    # Load configuration from Config class (from config.py)
    app.config.from_object(Config)
    # Load test config if running tests
    if os.environ.get('FLASK_ENV') == 'testing':
        app.config.from_object(TestingConfig)

    # Initialize the database (SQLAlchemy) and migration (Flask-Migrate)
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize Flask-Caching
    cache.init_app(app)

    # Enable CORS
    CORS(app)

    # Initialize Flask-RESTful API
    api = Api(app)

    # Player endpoints
    api.add_resource(PlayerResource, '/api/players', '/api/players/<string:player_id>')

    # Character endpoints
    api.add_resource(CharacterResource, '/api/characters', '/api/characters/<string:character_id>')

    # Map endpoints
    api.add_resource(MapResource,'/api/maps', '/api/maps/<string:map_id>')

    # Quest endpoints
    api.add_resource(QuestResource,'/api/quests', '/api/quests/<string:quest_id>')

    # Game logic endpoints
    api.add_resource(GameResource, '/api/game/<string:player_id>')

    # Health check endpoint
    api.add_resource(HealthResource, '/api/health/<string:player_id>')

    # Inventory endpoints
    api.add_resource(InventoryResource, '/api/inventory/<string:player_id>')

    # Safari event endpoints
    api.add_resource(StartSafariResource, '/api/start-safari')
    api.add_resource(ObserveWildlifeResource, '/api/observe-wildlife')
    api.add_resource(InteractWithLocalsResource, '/api/interact-with-locals')
    api.add_resource(HandleWeatherChangeResource, '/api/handle-weather-change')
    api.add_resource(TakePhotoResource, '/api/take-photo')
    api.add_resource(FindItemResource, '/api/find-item')
    api.add_resource(UseItemResource, '/api/use-item')
    api.add_resource(CompleteSafariResource, '/api/complete-safari')

    # CLI command to create tables
    @app.cli.command(name='create_tables')
    def create_tables():
        db.create_all() # Create all tables based on models
        print("Tables created successfully.")

    return app

app = create_app()

# AUTO-MIGRATION LOGIC FOR RENDER
with app.app_context():
    try:
        db.create_all()
        print("Database tables created.")
        
        # Check if characters exist, if not, seed the DB
        from models.character import Character
        if not Character.query.first():
            print("No characters found. Seeding database...")
            # Import seed functions
            from seed import seed_characters, seed_maps, seed_players, seed_quests
            # Run seeders
            characters = seed_characters()
            maps = seed_maps()
            # We don't necessarily need dummy players/quests for the game to work, 
            # but characters/maps are essential.
            print("Database seeded successfully!")
    except Exception as e:
        print(f"Error during startup migration: {e}")

if __name__ == "__main__":
    # Create Flask app instance and run the server
    app.run(debug=True, port= 5555)
