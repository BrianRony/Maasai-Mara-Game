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
        
        self.animals = [
            {'name': 'Lion', 'danger': 8, 'rare': False, 'desc': 'The king of the beasts.'},
            {'name': 'Elephant', 'danger': 7, 'rare': False, 'desc': 'A massive bull elephant with giant tusks.'},
            {'name': 'Black Rhino', 'danger': 9, 'rare': True, 'desc': 'An critically endangered solitary browser.'},
            {'name': 'Leopard', 'danger': 8, 'rare': True, 'desc': 'A silent shadow in the acacia trees.'},
            {'name': 'Cheetah', 'danger': 5, 'rare': False, 'desc': ' The fastest land animal.'},
            {'name': 'Buffalo', 'danger': 9, 'rare': False, 'desc': 'The widowmaker. Grumpy and dangerous.'},
            {'name': 'Hippo', 'danger': 10, 'rare': False, 'desc': 'Territorial and deadly in the water.'},
            {'name': 'Giraffe', 'danger': 2, 'rare': False, 'desc': 'A towering giant eating from the treetops.'},
            {'name': 'Pangolin', 'danger': 0, 'rare': True, 'desc': 'A shy, scaly anteater. Extremely rare!'},
        ]
        
        self.weather_conditions = ['scorching sun', 'monsoon rain', 'dust storm', 'perfect breeze', 'thick fog', 'thunderstorm']
        
        self.items = {
            'common': ['water bottle', 'binoculars', 'camera', 'snack', 'first aid kit', 'safari hat'],
            'Adventurer': ['ancient map', 'compass', 'climbing gear', 'flare gun', 'multi-tool'],
            'Hunter': ['rifle', 'ammunition', 'hunting knife', 'ghillie suit', 'decoys'],
            'Warden': ['radio', 'tranquilizer gun', 'veterinary kit', 'drone', 'anti-venom']
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
        status = self.get_player_status()
        
        # Game Over Check
        if status.get('health', 0) <= 0:
            success = False
            # Ensure health is not negative in display
            status['health'] = 0
            
        return {
            'success': success,
            'message': message,
            'updated_stats': status
        }

    def start_safari(self):
        # Fix: Fetch by name to avoid JSON comparison error
        self.player.current_location = Map.query.filter_by(location_name="Savannah Plains").first()
        character_type = self.player.character.character_type
        starting_item = self.items[character_type][0]
        
        self.inventory_resource.update_inventory(self.player.uuid, starting_item, 'add')
        
        intro_text = {
            'Adventurer': "You adjust your backpack. The horizon is endless. What secrets does it hold?",
            'Hunter': "You check your rifle bolt. Smooth. The Mara is wild, and you are ready.",
            'Warden': "You tune your radio. The rangers report activity in Sector 4. Time to patrol."
        }

        return {
            'message': f"{intro_text.get(character_type, 'Welcome to the Mara.')} You have a {starting_item}.",
            'stats': self.get_player_status(),
            'startingItem': starting_item
        }

    def get_observable_wildlife(self):
        animal_data = random.choice(self.animals)
        return {'name': animal_data['name'], 'description': animal_data['desc']}
    

    def observe_wildlife(self):
        if self._get_health_safe() <= 0: return self._build_response(False, "You are incapacitated.")

        animal_obj = random.choice(self.animals)
        animal = animal_obj['name']
        danger_level = animal_obj['danger']
        is_rare = animal_obj['rare']
        
        character_type = self.player.character.character_type
        inventory_response = self.inventory_resource.get_inventory(self.player.uuid)
        inventory = inventory_response[0].get('inventory', []) if isinstance(inventory_response, tuple) else inventory_response.get('inventory', [])
        
        base_score = 15 if is_rare else 10
        health_change = 0
        message = ""

        # SCENARIO GENERATION
        scenarios = [
            f"The {animal} is sleeping under a tree.",
            f"Suddenly! A {animal} bursts from the bushes!",
            f"You spot a {animal} drinking at a watering hole.",
            f"A {animal} is staring right at you."
        ]
        scenario = random.choice(scenarios)

        # 1. SPECIAL INTERACTION: WARDEN + RARE/INJURED
        if character_type == 'Warden' and random.random() < 0.3:
            if 'veterinary kit' in inventory or 'tranquilizer gun' in inventory:
                self.player.score += 60
                return self._build_response(True, f"HEROIC ACT: You found an injured {animal} caught in a snare. Using your gear, you sedated and treated it. +60 points!")
        
        # 2. SPECIAL INTERACTION: HUNTER + DANGEROUS
        if character_type == 'Hunter' and danger_level >= 8 and random.random() < 0.3:
            if 'rifle' in inventory:
                self.player.score += 50
                health_change = -5
                return self._build_response(True, f"ADRENALINE: The {animal} charged! You fired a warning shot and held your ground. It backed off. +50 points, -5 health (stress).")

        # 3. SPECIAL INTERACTION: ADVENTURER + HIDDEN
        if character_type == 'Adventurer' and is_rare:
            self.player.score += 70
            return self._build_response(True, f"DISCOVERY: You found a secret path leading to a nesting {animal}. This has never been mapped before! +70 points!")

        # STANDARD LOGIC
        if danger_level > 6:
            # High Danger Logic
            if character_type == 'Adventurer':
                if 'camera' in inventory: 
                    message = f"{scenario} You risked it all for the shot! +30 points, -10 health (scrapes)."
                    self.player.score += 30; health_change = -10
                else:
                    message = f"{scenario} It's too dangerous! You ran away. -20 health."
                    health_change = -20
            
            elif character_type == 'Hunter':
                 message = f"{scenario} You utilized your tracking knowledge to stay downwind. Safe. +20 points."
                 self.player.score += 20
            
            elif character_type == 'Warden':
                 message = f"{scenario} You noted its aggressive behavior in your log. +25 points."
                 self.player.score += 25
                 health_change = -5 # Minor risk

        else:
            # Low Danger Logic
            if 'binoculars' in inventory:
                message = f"You watched the {animal} from afar. Peaceful. +15 points."
                self.player.score += 15
            else:
                message = f"You got close to the {animal}. It was a magical moment. +10 points."
                self.player.score += 10

        self.health_resource.update_health(self.player.uuid, health_change)
        return self._build_response(True, message)


    def interact_with_locals(self):
        if self._get_health_safe() <= 0: return self._build_response(False, "You are incapacitated.")
        
        current_health = self._get_health_safe()
        character_type = self.player.character.character_type
        
        # HOSPITALITY MECHANIC (Life Saver)
        if current_health < 30:
            heal_amount = 50
            self.health_resource.update_health(self.player.uuid, heal_amount)
            return self._build_response(True, "The village elders see your wounds. They take you in, apply traditional herbs, and feed you warm broth. You are saved! +50 Health.")

        # TRADE / GIFT MECHANIC
        gift_roll = random.random()
        if gift_roll < 0.25:
            # They give you something
            items = ['snack', 'water bottle', 'spear', 'beaded necklace']
            gift = random.choice(items)
            self.inventory_resource.update_inventory(self.player.uuid, gift, 'add')
            return self._build_response(True, f"The Maasai welcome you warmly. An elder hands you a {gift} as a token of friendship. (Item added to inventory)")

        # Standard Interactions with Flavor
        if character_type == 'Adventurer':
            msg = "You show them your map. They laugh and show you a 'shortcut' that isn't on any paper."
            points = 25; hp = 5
        elif character_type == 'Hunter':
            msg = "You engage in a spear-throwing contest with the warriors. You didn't win, but you earned their respect."
            points = 30; hp = -5 # Fatigue
        elif character_type == 'Warden':
            msg = "You deliver medical supplies to the village. The chief thanks you for protecting their cattle from lions."
            points = 40; hp = 10
        else:
            msg = "You sit by the fire and listen to ancient stories of when the earth was young."
            points = 20; hp = 5

        self.player.score += points
        self.health_resource.update_health(self.player.uuid, hp)
        return self._build_response(True, f"{msg} +{points} pts, {hp} health.")

    def handle_weather_change(self):
        if self._get_health_safe() <= 0: return self._build_response(False, "You are incapacitated.")

        new_weather = random.choice(self.weather_conditions)
        character_type = self.player.character.character_type
        
        health_change = 0
        msg = ""

        if new_weather == 'dust storm':
            health_change = -15
            msg = "A blinding dust storm hits! Visibility is zero. You choke on the grit. -15 health."
            if 'safari hat' in self.player.inventory: # hypothetical check
                health_change = -5
                msg += " (Your hat helped!)"
        
        elif new_weather == 'monsoon rain':
            if character_type == 'Warden':
                 msg = "Heavy rains. Good for the ecosystem, bad for driving. You navigate the mud expertly."
            else:
                 health_change = -10
                 msg = " torrential rain turns the roads to rivers. You are soaked and shivering. -10 health."

        elif new_weather == 'scorching sun':
             if 'water bottle' in self.player.inventory:
                 msg = "It's brutally hot, but you have water. You stay hydrated."
             else:
                 health_change = -12
                 msg = "The African sun beats down relentlessly. You are dehydrated. -12 health."

        elif new_weather == 'perfect breeze':
            health_change = 10
            msg = "A cool breeze blows across the savanna. It lifts your spirits. +10 health."

        else:
            msg = f"The weather shifts to {new_weather}."

        self.health_resource.update_health(self.player.uuid, health_change)
        return self._build_response(True, msg)

    def take_photo(self):
        if self._get_health_safe() <= 0: return self._build_response(False, "You are incapacitated.")

        # Determine SUBJECT quality
        roll = random.random()
        if roll < 0.1:
            subject = "The Great Migration (River Crossing)"
            quality = "Legendary"
            score = 100
        elif roll < 0.4:
            subject = "A kill in progress"
            quality = "Rare"
            score = 50
        else:
            subject = "A sleeping lion"
            quality = "Common"
            score = 15

        inventory_response = self.inventory_resource.get_inventory(self.player.uuid)
        inventory = inventory_response[0].get('inventory', []) if isinstance(inventory_response, tuple) else inventory_response.get('inventory', [])
        
        if 'camera' in inventory:
            if 'drone' in inventory: # Warden item
                score += 20
                msg = f"AERIAL SHOT! You used your drone to capture {subject} from above. +{score} points."
            else:
                msg = f"Click! You captured a {quality} photo of {subject}. +{score} points."
            
            self.player.score += score
            return self._build_response(True, msg)
        else:
            return self._build_response(False, f"You witness {subject}, but without a camera, it's just a memory.")

    def find_item(self):
        if self._get_health_safe() <= 0: return self._build_response(False, "You are incapacitated.")

        character_type = self.player.character.character_type
        
        # Risk vs Reward
        roll = random.random()
        
        if roll < 0.2:
            # BAD EVENT
            damage = -15
            self.health_resource.update_health(self.player.uuid, damage)
            return self._build_response(True, "You stick your hand in a hollow log looking for supplies... A BLACK MAMBA strikes! -15 health.")
        
        elif roll < 0.3:
            # FLAVOR EVENT (No Item)
            return self._build_response(True, "You found an old poacher's camp. It's abandoned. Nothing useful here, just bad memories.")

        else:
            # FIND ITEM
            if character_type == 'Adventurer' and random.random() < 0.5:
                item = 'ancient idol' # Score item
                self.player.score += 50
                return self._build_response(True, "JACKPOT! You found an ancient tribal idol buried in the sand. It belongs in a museum! +50 points.")
            
            common_items = self.items['common']
            item = random.choice(common_items)
            
            try:
                self.inventory_resource.update_inventory(self.player.uuid, item, 'add')
                return self._build_response(True, f"You scavenged a {item}! Added to inventory.")
            except:
                return self._build_response(False, "Inventory full.")

    def use_item(self, item_name):
        if self._get_health_safe() <= 0: return self._build_response(False, "You are incapacitated.")
        
        # "Use" logic is mostly standard, but let's add flavor
        try:
            self.inventory_resource.update_inventory(self.player.uuid, item_name, 'remove')
            
            msg = f"You used {item_name}."
            
            if item_name == 'first aid kit':
                heal = 40
                self.health_resource.update_health(self.player.uuid, heal)
                msg = "You dressed your wounds. Feeling much better. +40 HP."
            
            elif item_name == 'water bottle':
                heal = 15
                self.health_resource.update_health(self.player.uuid, heal)
                msg = "Cool, refreshing water. +15 HP."
                
            elif item_name == 'flare gun': # Adventurer
                self.player.score += 20
                msg = "You fired a flare to signal your position. A ranger plane dipped its wings in acknowledgement. +20 pts."
            
            elif item_name == 'ancient idol':
                self.player.score += 50
                msg = "You admire the idol. It's worth a fortune in points."

            return self._build_response(True, msg)

        except Exception as e:
            return self._build_response(False, f"Could not use item: {str(e)}")

    def complete_safari(self):
        # Even if dead, you reach this screen to see stats
        character_type = self.player.character.character_type
        final_score = self.player.score
        final_health = self._get_health_safe()
        
        inventory_response = self.inventory_resource.get_inventory(self.player.uuid)
        inventory = inventory_response[0].get('inventory', []) if isinstance(inventory_response, tuple) else inventory_response.get('inventory', [])

        if final_health <= 0:
            return self._build_response(False, f"TRAGEDY. Your safari ended in disaster. The Mara claims another soul.\nFinal Score: {final_score}")

        achievements = []
        if final_score > 400: achievements.append("Legend of the Mara")
        if final_health > 90: achievements.append("Survivor")
        if 'ancient idol' in inventory: achievements.append("Tomb Raider")
        if 'veterinary kit' in inventory and character_type == 'Warden': achievements.append("Dr. Doolittle")

        msg = f"MISSION SUCCESS!\nClass: {character_type}\nScore: {final_score}\nHealth: {final_health}\n\nAchievements: {', '.join(achievements)}"
        
        return self._build_response(True, msg)
