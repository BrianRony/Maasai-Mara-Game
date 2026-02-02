import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import SafariLayout from "./SafariLayout";

function Player() {
  const [name, setName] = useState('');
  const [characterType, setCharacterType] = useState('Adventurer');
  const [existingPlayers, setExistingPlayers] = useState([]);
  const [selectedPlayerId, setSelectedPlayerId] = useState('');
  const [mode, setMode] = useState('new'); // 'new' or 'existing'
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // Fetch existing players on mount
  useEffect(() => {
    fetchPlayers();
  }, []);

  const fetchPlayers = async () => {
    try {
      const response = await fetch('/api/players');
      if (response.ok) {
        const data = await response.json();
        if (Array.isArray(data)) {
          setExistingPlayers(data);
        } else {
          console.error("Expected array of players, got:", data);
          setExistingPlayers([]);
        }
      }
    } catch (err) {
      console.error("Failed to load players", err);
    }
  };

  const handleCreateSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('/api/players', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, character_type: characterType }),
      });

      if (response.ok) {
        const data = await response.json();
        navigate(`/game/${data.uuid}`);
      } else {
        const err = await response.json();
        setError(err.message || 'Failed to create player');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    }
  };

  const handleExistingSubmit = (e) => {
    e.preventDefault();
    if (selectedPlayerId) {
      navigate(`/game/${selectedPlayerId}`);
    }
  };

  return (
    <SafariLayout title="Who are you?" subtitle="Choose your path">
      <div className="max-w-md mx-auto">
        
        {/* Mode Toggle Tabs */}
        <div className="flex mb-8 bg-gray-900 rounded-lg p-1">
          <button
            onClick={() => setMode('new')}
            className={`flex-1 py-2 rounded-md font-bold transition-all ${
              mode === 'new' 
                ? 'bg-yellow-600 text-white shadow-md' 
                : 'text-gray-400 hover:text-white'
            }`}
          >
            New Explorer
          </button>
          <button
            onClick={() => setMode('existing')}
            className={`flex-1 py-2 rounded-md font-bold transition-all ${
              mode === 'existing' 
                ? 'bg-yellow-600 text-white shadow-md' 
                : 'text-gray-400 hover:text-white'
            }`}
          >
            Returning Player
          </button>
        </div>

        {/* NEW PLAYER FORM */}
        {mode === 'new' && (
          <form onSubmit={handleCreateSubmit} className="space-y-6">
            <div>
              <label className="block text-yellow-500 text-sm font-bold mb-2 uppercase tracking-wide">
                Explorer Name
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full bg-gray-900 text-white border-2 border-gray-600 rounded-lg py-3 px-4 focus:outline-none focus:border-yellow-500 focus:ring-1 focus:ring-yellow-500 transition-colors"
                placeholder="Enter your name..."
                required
              />
            </div>

            <div>
              <label className="block text-yellow-500 text-sm font-bold mb-2 uppercase tracking-wide">
                Select Class
              </label>
              <div className="relative">
                <select
                  value={characterType}
                  onChange={(e) => setCharacterType(e.target.value)}
                  className="w-full bg-gray-900 text-white border-2 border-gray-600 rounded-lg py-3 px-4 appearance-none focus:outline-none focus:border-yellow-500 focus:ring-1 focus:ring-yellow-500 transition-colors"
                >
                  <option value="Adventurer">Adventurer (Balanced)</option>
                  <option value="Hunter">Hunter (Combat Focus)</option>
                  <option value="Warden">Warden (Survival Focus)</option>
                </select>
                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-400">
                  <svg className="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                    <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/>
                  </svg>
                </div>
              </div>
              <p className="text-gray-400 text-xs mt-2 italic">
                {characterType === 'Adventurer' && "Starts with Map & Compass."}
                {characterType === 'Hunter' && "Starts with Rifle & Knife."}
                {characterType === 'Warden' && "Starts with Medkit & Radio."}
              </p>
            </div>

            <button
              type="submit"
              disabled={!name.trim()}
              className={`w-full font-bold py-4 px-8 rounded-xl shadow-lg transform transition text-lg
                ${name.trim() 
                  ? 'bg-green-600 hover:bg-green-500 hover:scale-105 text-white' 
                  : 'bg-gray-700 text-gray-500 cursor-not-allowed'}`}
            >
              Begin Adventure 🚀
            </button>
          </form>
        )}

        {/* EXISTING PLAYER FORM */}
        {mode === 'existing' && (
          <form onSubmit={handleExistingSubmit} className="space-y-6">
            <div>
              <label className="block text-yellow-500 text-sm font-bold mb-2 uppercase tracking-wide">
                Select Explorer
              </label>
              <div className="relative">
                <select
                  value={selectedPlayerId}
                  onChange={(e) => setSelectedPlayerId(e.target.value)}
                  className="w-full bg-gray-900 text-white border-2 border-gray-600 rounded-lg py-3 px-4 appearance-none focus:outline-none focus:border-yellow-500 focus:ring-1 focus:ring-yellow-500 transition-colors"
                  size="5" // Show list style
                >
                  <option value="" disabled className="text-gray-500">-- Choose a saved game --</option>
                  {existingPlayers.length === 0 && (
                    <option disabled className="text-gray-500">No saved games found.</option>
                  )}
                  {existingPlayers.map(player => (
                    <option key={player.uuid} value={player.uuid} className="py-1">
                      {player.name} ({player.character?.character_type || 'Unknown'}) - Score: {player.score}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <button
              type="submit"
              disabled={!selectedPlayerId}
              className={`w-full font-bold py-4 px-8 rounded-xl shadow-lg transform transition text-lg
                ${selectedPlayerId
                  ? 'bg-blue-600 hover:bg-blue-500 hover:scale-105 text-white' 
                  : 'bg-gray-700 text-gray-500 cursor-not-allowed'}`}
            >
              Continue Journey ↺
            </button>
          </form>
        )}

        {error && (
          <div className="mt-6 bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded-lg text-sm text-center">
            {error}
          </div>
        )}

      </div>
    </SafariLayout>
  );
}

export default Player;
