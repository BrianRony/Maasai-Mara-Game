import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Player() {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [characterType, setCharacterType] = useState('');
  const [message, setMessage] = useState('');
  const [existingPlayers, setExistingPlayers] = useState([]);
  const [selectedPlayer, setSelectedPlayer] = useState('');

  // Fetch the list of existing players
  useEffect(() => {
    fetchExistingPlayers();
  }, []);

  const fetchExistingPlayers = async () => {
    try {
      const response = await fetch('/api/players');
      const data = await response.json();
      setExistingPlayers(data);
    } catch (error) {
      console.error('Error fetching existing players:', error);
    }
  };

  // Handle form submission for a new player
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/players', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: name,
          character_type: characterType,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        setMessage(`Player added successfully! Starting game...`);
        navigate(`/game/${data.uuid}`);  // Redirect to the game for the new player
      } else {
        setMessage(
          `Error adding player: ${data.message}. If this player exists, please check Returning Players to continue the game.`
        );
      }
    } catch (error) {
      setMessage(`Error adding player: ${error.message}`);
    }
  };

  // Handle selection of an existing player from the dropdown
  const handlePlayerSelection = () => {
    if (selectedPlayer) {
      navigate(`/game/${selectedPlayer}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center p-6">
      <div className="bg-gray-800 p-8 rounded-lg shadow-lg w-full max-w-lg">
        {/* Form to add a new player */}
        <h2 className="text-3xl font-bold text-yellow-400 mb-6 text-center">Add New Player</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-300">Name:</label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="mt-1 block w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-yellow-500 focus:border-yellow-500 sm:text-sm"
            />
          </div>
          <div>
            <label htmlFor="characterType" className="block text-sm font-medium text-gray-300">Character Type:</label>
            <select
              id="characterType"
              value={characterType}
              onChange={(e) => setCharacterType(e.target.value)}
              required
              className="mt-1 block w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-yellow-500 focus:border-yellow-500 sm:text-sm"
            >
              <option value="">Select a character type</option>
              <option value="Adventurer">Adventurer</option>
              <option value="Hunter">Hunter</option>
              <option value="Warden">Warden</option>
            </select>
          </div>
          <div>
            <button
              type="submit"
              className="w-full bg-yellow-500 hover:bg-yellow-600 text-black font-bold py-3 px-6 rounded-md transition duration-300"
            >
              Add Player & Start Game
            </button>
          </div>
        </form>
        {message && <p className="mt-4 text-center text-yellow-400">{message}</p>}

        {/* Returning players section */}
        <div className="mt-8">
          <h3 className="text-2xl font-bold text-yellow-400 mb-4">Returning Players</h3>
          {existingPlayers.length > 0 ? (
            <>
              <select
                value={selectedPlayer}
                onChange={(e) => setSelectedPlayer(e.target.value)}
                className="w-full px-4 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-yellow-500 focus:border-yellow-500 sm:text-sm"
              >
                <option value="">Select a returning player</option>
                {existingPlayers.map((player) => (
                  <option key={player.uuid} value={player.uuid}>
                    {player.name} - {player.character_type}
                  </option>
                ))}
              </select>
              <button
                onClick={handlePlayerSelection}
                disabled={!selectedPlayer}
                className={`mt-4 w-full ${
                  selectedPlayer
                    ? 'bg-yellow-500 hover:bg-yellow-600 text-black'
                    : 'bg-gray-500 text-gray-300 cursor-not-allowed'
                } font-bold py-3 px-6 rounded-md transition duration-300`}
              >
                Continue Game
              </button>
            </>
          ) : (
            <p className="text-gray-400">No existing players found.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Player;
