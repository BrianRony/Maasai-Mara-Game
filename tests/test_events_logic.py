import pytest
from server.services.events_logic import MaasaiMaraEventsLogic
from unittest.mock import MagicMock
from server.models.map import Player
from server.models.map import Map

@pytest.fixture
def mock_player():
    """A mock player fixture for testing"""
    player = MagicMock(spec=Player)
    player.uuid = "test-player-id"
    player.character.character_type = "Adventurer"
    player.score = 0
    player.health = 100
    return player

@pytest.fixture
def mock_map():
    """A mock map fixture for testing"""
    map_instance = MagicMock(spec=Map)
    map_instance.coordinates = {"x": 0, "y": 0}
    return map_instance

@pytest.fixture
def event_logic(mock_player):
    """A fixture for MaasaiMaraEventsLogic instance"""
    event_logic = MaasaiMaraEventsLogic(mock_player.uuid)
    event_logic.player = mock_player
    return event_logic

def test_start_safari(event_logic, mock_map):
    """Test the start_safari method"""
    Map.query.filter_by.return_value.first.return_value = mock_map
    success, message = event_logic.start_safari()
    assert success is True
    assert "Your safari adventure begins" in message
    assert event_logic.player.current_location == mock_map

def test_observe_wildlife(event_logic):
    """Test the observe_wildlife method"""
    event_logic.inventory_resource.get.return_value = {'inventory': ['camera']}
    success, message = event_logic.observe_wildlife()
    assert success is True
    assert "captured an amazing photo" in message
    assert event_logic.player.score > 0

def test_interact_with_locals(event_logic):
    """Test the interact_with_locals method"""
    success, message = event_logic.interact_with_locals()
    assert success is True
    assert "learned about Maasai customs" in message

def test_handle_weather_change(event_logic):
    """Test handle_weather_change method"""
    event_logic.health_resource.get.return_value = {'health': 100}
    message = event_logic.handle_weather_change()
    assert "weather" in message

def test_find_item(event_logic):
    """Test find_item method"""
    event_logic.inventory_resource.put.return_value = (True, 200)
    success, message = event_logic.find_item()
    assert success is True
    assert "found" in message

def test_complete_safari(event_logic):
    """Test complete_safari method"""
    event_logic.player.score = 300
    success, message = event_logic.complete_safari()
    assert success is True
    assert "completed your Maasai Mara safari" in message
