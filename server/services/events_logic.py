from services.game_service import GameService
from resources.health_handler_resource import HealthResource
from resources.inventory_handler_resource import InventoryResource
from models.player import Player
from models.map import Map
from extension import db
import random
from config import Config

class MaasaiMaraEventsLogic(GameService):
    def __init__(self, player_id):
        super().__init__(player_id)
        if not self.player:
            raise ValueError(f"No player found with id {player_id}")
        self.health_resource = HealthResource()
        self.inventory_resource = InventoryResource()
        self.animals = ['lion', 'elephant', 'giraffe', 'zebra', 'wildebeest', 'cheetah']
        self.weather_conditions = ['sunny', 'rainy', 'windy', 'misty']
        self.items = {
            'common': ['water bottle', 'binoculars', 'camera', 'snack', 'first aid kit'],
            'Adventurer': ['map', 'compass', 'rope', 'flashlight', 'multi-tool'],
            'Hunter': ['rifle', 'ammunition', 'hunting knife', 'camouflage gear', 'animal calls'],
            'Warden': ['radio', 'tranquilizer gun', 'wildlife guide', 'GPS tracker', 'rescue flares']
        }
        self.default_start_location_coordinates = getattr(Config, 'DEFAULT_START_LOCATION_COORDINATES', {"x": 0, "y": 0})

    def _get_health_safe(self):
        """Helper to extract health value from resource response tuple."""
        response = self.health_resource.get_health(self.player.uuid)
        if isinstance(response, tuple):
            return response[0].get('health', 0)
        return response.get('health', 0)

    def _build_response(self, success, message):
        """Standardized response helper with updated stats."""
        return {
            'success': success,
            'message': message,
            'updated_stats': self.get_player_status()
        }

    def start_safari(self):
        self.player.current_location = Map.query.filter_by(coordinates=self.default_start_location_coordinates).first()
        character_type = self.player.character.character_type
        starting_item = self.items[character_type][0]
        
        self.inventory_resource.update_inventory(self.player.uuid, starting_item, 'add')
        
        return {
            'message': f"Welcome to the Maasai Mara! Your safari adventure begins. You've been equipped with a {starting_item}.",
            'stats': self.get_player_status(),
            'startingItem': starting_item
        }

    def get_observable_wildlife(self):
        animal = random.choice(self.animals)
        return {'name': animal, 'description': f'A majestic {animal} in the wild.'}
    

    def observe_wildlife(self):
        animal = self.get_observable_wildlife()['name']
        character_type = self.player.character.character_type
        
        inventory_response = self.inventory_resource.get_inventory(self.player.uuid)
        inventory = inventory_response[0].get('inventory', []) if isinstance(inventory_response, tuple) else inventory_response.get('inventory', [])
        
        base_score = 10
        health_change = 0
        message = ""

        if character_type == 'Adventurer':
            if 'camera' in inventory:
                self.player.score += base_score + 10
                health_change = -5
                message = f"You captured an amazing photo of a {animal}! +20 points, -5 health"
            else:
                self.player.score += base_score
                health_change = -2
                message = f"You got closer to the {animal} and documented it in your journal. +10 points, -2 health"
        elif character_type == 'Hunter':
            if 'binoculars' in inventory:
                self.player.score += base_score + 15
                health_change = -3
                message = f"You tracked a {animal} from a safe distance. +25 points, -3 health"
            else:
                self.player.score += base_score
                health_change = -5
                message = f"You observed a {animal}'s behavior up close. +10 points, -5 health"
        elif character_type == 'Warden':
            if 'wildlife guide' in inventory:
                self.player.score += base_score + 20
                health_change = -2
                message = f"You identified a rare {animal} and updated conservation records. +30 points, -2 health"
            else:
                self.player.score += base_score
                health_change = -4
                message = f"You ensured the safety of a {animal} in its natural habitat. +10 points, -4 health"
        else:
            self.player.score += base_score
            health_change = -5
            message = f"You got a closer look at the {animal}! +10 points, -5 health"

        self.health_resource.update_health(self.player.uuid, health_change)
        return self._build_response(True, message)


    def interact_with_locals(self):
        character_type = self.player.character.character_type
        
        if character_type == 'Adventurer':
            interaction = "You participated in a traditional Maasai ceremony and learned about their customs."
            points = 25
            health_increase = 10
        elif character_type == 'Hunter':
            interaction = "You exchanged hunting techniques with local Maasai warriors."
            points = 20
            health_increase = 5
        elif character_type == 'Warden':
            interaction = "You collaborated with local Maasai on wildlife conservation efforts."
            points = 30
            health_increase = 15
        else:
            interaction = random.choice([
                "You learned about Maasai culture.",
                "You participated in a traditional dance.",
                "You helped herd cattle with the Maasai."
            ])
            points = 20
            health_increase = 5

        self.player.score += points
        self.health_resource.update_health(self.player.uuid, health_increase)
        
        return self._build_response(True, f"{interaction} +{points} points. Your health increased by {health_increase}.")

    def handle_weather_change(self):
        new_weather = random.choice(self.weather_conditions)
        character_type = self.player.character.character_type
        current_health = self._get_health_safe()

        health_change = 0
        if new_weather == 'rainy':
            if character_type == 'Hunter':
                health_change = -2
            elif character_type == 'Adventurer':
                health_change = -7
            else:  # Warden
                health_change = -5
            
            self.health_resource.update_health(self.player.uuid, health_change)
            msg = f"It started raining. Your health changed by {health_change}. Current health: {current_health + health_change}"

        elif new_weather == 'sunny':
            if character_type == 'Hunter':
                health_change = 7
            elif character_type == 'Adventurer':
                health_change = 3
            else:  # Warden
                health_change = 5
            
            self.health_resource.update_health(self.player.uuid, health_change)
            msg = f"The sun is shining. Your health increased by {health_change}. Current health: {current_health + health_change}"

        else:
            if character_type == 'Hunter':
                msg = f"The weather changed to {new_weather}. As a Hunter, you're well-prepared for any conditions!"
            elif character_type == 'Adventurer':
                msg = f"The weather changed to {new_weather}. Be extra cautious, Adventurer!"
            else:  # Warden
                msg = f"The weather changed to {new_weather}. As a Warden, you're ready to face the elements!"
        
        return self._build_response(True, msg)

    def take_photo(self):
        subjects = self.animals + ['landscape', 'sunset', 'Maasai village']
        subject = random.choice(subjects)
        inventory_response = self.inventory_resource.get_inventory(self.player.uuid)
        inventory = inventory_response[0].get('inventory', []) if isinstance(inventory_response, tuple) else inventory_response.get('inventory', [])
        
        character_type = self.player.character.character_type
        
        success = False
        message = ""

        if 'camera' in inventory:
            success = True
            if character_type == 'Adventurer':
                self.player.score += 20
                message = f"You captured a breathtaking shot of a {subject}. Your adventurous spirit shines through the image! +20 points"
            elif character_type == 'Hunter':
                self.player.score += 15
                message = f"You snapped a rare photo of a {subject} in its natural habitat. Your tracking skills paid off! +15 points"
            elif character_type == 'Warden':
                self.player.score += 25
                message = f"You documented a {subject} for conservation purposes. This photo will greatly aid research efforts! +25 points"
            else:
                self.player.score += 15
                message = f"You took a beautiful photo of a {subject} with your camera. +15 points"
        else:
            success = False
            if character_type == 'Adventurer':
                message = "You wish you had a camera to capture this amazing moment!"
            elif character_type == 'Hunter':
                message = "A camera would be useful for scouting and documenting wildlife patterns."
            elif character_type == 'Warden':
                message = "A camera would be a valuable tool for your conservation work. Consider acquiring one."
            else:
                message = "You don't have a camera to take photos."
        
        return self._build_response(success, message)

    def find_item(self):
        character_type = self.player.character.character_type
        common_items = self.items['common']
        specific_items = self.items[character_type]
        if random.random() < 0.7:
            item = random.choice(specific_items)
        else:
            item = random.choice(common_items)
        
        try:
            self.inventory_resource.update_inventory(self.player.uuid, item, 'add')
            if item in specific_items:
                msg = f"You found a {item}! This will be particularly useful for a {character_type}. Added to your inventory."
            else:
                msg = f"You found a {item}! It has been added to your inventory."
            return self._build_response(True, msg)
        except ValueError as e:
            return self._build_response(False, f"You found a {item}, but couldn't take it: {str(e)}")
        except Exception as e:
             return self._build_response(False, f"Error finding item: {str(e)}")


    def use_item(self, item_name):
        character_type = self.player.character.character_type
        
        try:
            self.inventory_resource.update_inventory(self.player.uuid, item_name, 'remove')
            
            message = ""
            if item_name == 'water bottle':
                health_increase = 15 if character_type == 'Adventurer' else 10
                self.health_resource.update_health(self.player.uuid, health_increase)
                message = f"You drank from your water bottle. +{health_increase} health"

            elif item_name == 'snack':
                health_increase = 8 if character_type == 'Hunter' else 5
                self.health_resource.update_health(self.player.uuid, health_increase)
                message = f"You ate a snack. +{health_increase} health"

            elif item_name == 'first aid kit':
                health_increase = 25 if character_type == 'Warden' else 20
                self.health_resource.update_health(self.player.uuid, health_increase)
                message = f"You used the first aid kit. +{health_increase} health"

            elif item_name in self.items[character_type]:
                self.player.score += 10
                message = f"You skillfully used the {item_name}. As a {character_type}, you gain +10 points!"

            else:
                message = f"You used the {item_name}."
            
            return self._build_response(True, message)

        except ValueError:
            return self._build_response(False, f"You don't have a {item_name} in your inventory.")
        except Exception as e:
            return self._build_response(False, f"Could not use item: {str(e)}")


    def complete_safari(self):
        character_type = self.player.character.character_type
        final_score = self.player.score
        final_health = self._get_health_safe()
        
        inventory_response = self.inventory_resource.get_inventory(self.player.uuid)
        inventory = inventory_response[0].get('inventory', []) if isinstance(inventory_response, tuple) else inventory_response.get('inventory', [])

        achievements = []
        if final_score > 200:
            achievements.append("Master Explorer")
        if final_health > 90:
            achievements.append("Survival Expert")
        if len(inventory) >= 5:
            achievements.append("Resourceful Traveler")
        
        # ... (Achievement logic remains same) ...
        # Just copying logic to be safe, but returning standard dict
        if character_type == 'Adventurer':
            if 'camera' in inventory and final_score > 150:
                achievements.append("Wildlife Photographer")
            if final_score > 250:
                achievements.append("Thrill Seeker")
        elif character_type == 'Hunter':
            if 'binoculars' in inventory and final_score > 180:
                achievements.append("Expert Tracker")
            if final_health > 95:
                achievements.append("Wilderness Survivor")
        elif character_type == 'Warden':
            if 'wildlife guide' in inventory and final_score > 200:
                achievements.append("Conservation Champion")
            if len([item for item in inventory if item in self.items['Warden']]) >= 3:
                achievements.append("Well-Equipped Warden")

        character_message = {
            'Adventurer': "Your adventurous spirit has led you to great discoveries!",
            'Hunter': "Your tracking skills have proven invaluable in the wild!",
            'Warden': "Your dedication to conservation has made a real difference!"
        }.get(character_type, "")
        
        msg = f"Congratulations, {character_type}! You've completed your Maasai Mara safari with a score of {final_score} and {final_health} health. {character_message}\nInventory: {', '.join(inventory)}.\nAchievements: {', '.join(achievements)}"
        
        return self._build_response(True, msg)
