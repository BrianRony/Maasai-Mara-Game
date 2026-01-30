from models.player import Player
from models.character import Character
from models.map import Map
from models.quest import Quest
from extension import db
import random

class GameService:
    def __init__(self, player_id):
        self.player = Player.query.get(player_id)
        if not self.player:
            raise ValueError(f"Player with id {player_id} not found.")

    def get_player_status(self):
        """Get the current status of the player."""
        return {
            'name': self.player.name,
            'health': self.player.health,
            'score': self.player.score,
            'inventory': self.player.inventory,
            'current_location': self.player.current_location.location_name if self.player.current_location else None,
            'current_quest': self.player.current_quest
        }

    def reset_game(self):
        """Reset the player's health, score, inventory, and active quest."""
        self.player.health = 100
        self.player.score = 0
        self.player.inventory = []
        self.player.current_quest = None
        db.session.commit()
        return True, "Game reset successfully"
    
    def save_game_state(self):
        """Save the player's current game state."""
        gameState ={'name': self.player.name,
                    'health': self.player.health,
                    'score': self.player.score,
                    'inventory': self.player.inventory,
                    'current_location': self.player.current_location.location_name if self.player.current_location else None,
                    'current_quest': self.player.current_quest}
        
        db.session.commit(gameState)
        return True, "Game saved successfully"

    def load_game_state(self, player_id):
        """Load the player's saved game state."""
        self.player = Player.query.get(player_id)
        if not self.player:
            return False, "Failed to load game state."
        return True, "Game loaded successfully"
    
    def handle_player_win(self):
        self.player.score = 1000
        self.player.health = 100
        return True, "Congratulations! You've completed your Maasai Mara safari with a score of 1000 and 100 health."
    
    def handle_player_quit(self):
        self.player.score = 0
        self.player.health = 0
        return True, "You've quit the game. Game over."
    
    def handle_player_restart(self):
        self.player.is_alive = True
        self.player.score = 0
        self.player.health = 100
        return True, "You've restarted the game. Your health is restored to 100."
    
    def handle_player_help(self):
        return True, "Available commands: move, interact, take photo, find item, use item, complete safari, quit, restart, help"

