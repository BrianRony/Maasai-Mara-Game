from app import create_app
from models.character import Character
from models.player import Player
from models.quest import Quest
from models.map import Map
from extension import db
from random import choice as rc
import uuid

app = create_app()

def seed_characters():
    characters = [
        Character(
            uuid=str(uuid.uuid4()),
            character_type="Adventurer",
            abilities="Exploration, Puzzle-solving",
            inventory=["Map", "Compass", "Torch"],
            description="Expert in exploration and navigating tricky landscapes."
        ),
        Character(
            uuid=str(uuid.uuid4()),
            character_type="Hunter",
            abilities="Combat, Tracking",
            inventory=["Bow", "Arrows", "Trap"],
            description="Skilled in combat and tracking wildlife."
        ),
        Character(
            uuid=str(uuid.uuid4()),
            character_type="Warden",
            abilities="Authority, Wildlife Protection",
            inventory=["Whistle", "Ranger Badge", "Medical Kit"],
            description="Uses authority to protect wildlife and enforce laws."
        )
    ]
    db.session.add_all(characters)
    db.session.commit()
    return characters

def seed_maps():
    maps = [
        Map(
            uuid=str(uuid.uuid4()),
            location_name="Savannah Plains",
            coordinates={"x": 0, "y": 0},
            description="Vast grasslands teeming with diverse wildlife.",
            quests_available=[]
        ),
        Map(
            uuid=str(uuid.uuid4()),
            location_name="Mara River",
            coordinates={"x": 10, "y": 5},
            description="Vital water source, famous for wildebeest crossings.",
            quests_available=[]
        ),
        Map(
            uuid=str(uuid.uuid4()),
            location_name="Acacia Forest",
            coordinates={"x": -5, "y": 8},
            description="Sparse woodland providing shelter for various animals.",
            quests_available=[]
        )
    ]
    db.session.add_all(maps)
    db.session.commit()
    return maps

def seed_players(characters, maps):
    players = [
        Player(
            uuid=str(uuid.uuid4()),
            name="Alex",
            health=100,
            score=0,
            inventory=["Water", "Food", "Binoculars"],
            current_quest=None,
            current_location_id=rc(maps).uuid,
            character_id=rc(characters).uuid
        ),
        Player(
            uuid=str(uuid.uuid4()),
            name="Sam",
            health=100,
            score=10,
            inventory=["Rope", "First Aid Kit", "Camera"],
            current_quest=None,
            current_location_id=rc(maps).uuid,
            character_id=rc(characters).uuid
        )
    ]
    db.session.add_all(players)
    db.session.commit()

def seed_quests(maps):
    quests = [
        Quest(
            uuid=str(uuid.uuid4()),
            title="Explore the Hidden Caves",
            description="Navigate underground tunnels to uncover lost treasures.",
            outcomes={
                "Adventurer": "Discovered ancient artifacts!",
                "Hunter": "Found rare animal tracks.",
                "Warden": "Rescued lost tourists."
            },
            is_completed=False,
            location_id=rc(maps).uuid
        ),
        Quest(
            uuid=str(uuid.uuid4()),
            title="Track the Elusive Leopard",
            description="Follow the trail of a rarely seen leopard.",
            outcomes={
                "Adventurer": "Captured amazing photos.",
                "Hunter": "Successfully tracked the leopard.",
                "Warden": "Ensured the leopard's safety."
            },
            is_completed=False,
            location_id=rc(maps).uuid
        )
    ]
    db.session.add_all(quests)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        print("Starting seed...")
        db.session.query(Player).delete()
        db.session.query(Quest).delete()
        db.session.query(Character).delete()
        db.session.query(Map).delete()

        characters = seed_characters()
        maps = seed_maps()
        seed_players(characters, maps)
        seed_quests(maps)

        print("Seeding completed successfully!")