import React, { useState, useEffect } from 'react';
import ChangeCharacterType from './ChangeCharacterType';

function StartSafari({ playerId, onComplete }) {
  const [message, setMessage] = useState('');
  const [characterType, setCharacterType] = useState('');
  const [showChangeType, setShowChangeType] = useState(false);
  const [playerStats, setPlayerStats] = useState(null);

  const fetchPlayerStats = async () => {
    try {
      // FIX: Fetch only the specific player, returns object directly
      const response = await fetch(`/api/players/${playerId}`);
      if (response.ok) {
        const data = await response.json();
        setPlayerStats(data);
      }
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  };

  useEffect(() => {
    fetchPlayerStats();
  }, [playerId]);

  const handleStartSafari = async () => {
    try {
      const response = await fetch('/api/start-safari', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_id: playerId, character_type: characterType }),
      });

      const data = await response.json();

      if (response.ok && data.stats && data.startingItem) {
        setMessage(data.message);
        onComplete({ ...data.stats, startingItem: data.startingItem });
      } else {
        setMessage(`Error: ${data.message}`);
      }
    } catch (error) {
      setMessage(`Error: ${error.message}`);
    }
  };

  const handleChangeCharacterType = async (type) => {
    setCharacterType(type);
    setShowChangeType(false);
    await fetchPlayerStats();
  };

  return (
    <div className="w-full text-center">
      <p className="text-gray-300 mb-6 italic">
        "The savanna calls your name..."
      </p>
      
      <div className="space-y-4">
        <button
          onClick={handleStartSafari}
          className="w-full bg-gradient-to-r from-yellow-500 to-yellow-600 hover:from-yellow-400 hover:to-yellow-500 text-black font-bold py-3 px-6 rounded-lg shadow-md transform transition hover:scale-105"
        >
          Start Safari
        </button>
        
        <button
          onClick={() => setShowChangeType(true)}
          className="w-full bg-gray-700 hover:bg-gray-600 text-gray-200 font-semibold py-2 px-4 rounded-lg transition"
        >
          Change Character Type
        </button>
      </div>

      {message && <p className="mt-4 text-yellow-400 font-semibold animate-pulse">{message}</p>}
      
      {showChangeType && (
        <div className="mt-4 border-t border-gray-700 pt-4">
          <ChangeCharacterType playerId={playerId} onChange={handleChangeCharacterType} />
        </div>
      )}
    </div>
  );
}

export default StartSafari;
