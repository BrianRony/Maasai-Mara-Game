import React, { useState, useEffect } from 'react';

import config from '../config';

const ObserveWildlife = ({ playerId, onComplete }) => {
  const [wildlife, setWildlife] = useState(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchWildlifeData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [playerId]);

  const fetchWildlifeData = async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/api/observe-wildlife?player_id=${playerId}`);
      if (response.ok) {
        const data = await response.json();
        if (data.wildlife) setWildlife(data.wildlife);
        else setMessage('No wildlife found.');
      }
      setLoading(false);
    } catch (error) {
      setMessage('Error loading wildlife.');
      setLoading(false);
    }
  };

  const handleObserve = async () => {
    try {
      const response = await fetch(`${config.API_BASE_URL}/api/observe-wildlife?player_id=${playerId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ player_id: playerId }),
      });

      const data = await response.json();

      if (data.success) {
        setMessage(data.message);
        setTimeout(() => {
          if (onComplete) onComplete(data.updated_stats);
        }, 6000); // 6s delay to read the outcome
      } else {
        setMessage(`${data.message}`);
        // If it's a game over (health <= 0), we must proceed to update stats so Game.js renders Game Over
        if (data.updated_stats && data.updated_stats.health <= 0) {
           setTimeout(() => {
              if (onComplete) onComplete(data.updated_stats);
           }, 4000);
        }
      }
    } catch (error) {
      setMessage(`Connection Error: ${error.message}`);
    }
  };

  return (
    <div className="w-full text-center">
      {loading ? (
        <p className="text-gray-400 animate-pulse">Scanning the horizon...</p>
      ) : wildlife ? (
        <div className="mb-8">
          <div className="text-6xl mb-4">🦁</div>
          <h3 className="text-2xl font-bold text-yellow-300 mb-2">{wildlife.name}</h3>
          <p className="text-gray-400 italic">"{wildlife.description}"</p>
        </div>
      ) : (
        <p className="text-red-400">{message}</p>
      )}

      {!message ? (
        <button
          onClick={handleObserve}
          className="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 px-6 rounded-lg shadow-lg transform transition hover:scale-105"
        >
          Observe Closely
        </button>
      ) : (
        <div className="mt-6 p-4 bg-gray-700/50 rounded-lg border border-yellow-600/50">
          <p className="text-yellow-300 font-medium">{message}</p>
          <p className="text-xs text-gray-400 mt-2">Proceeding...</p>
        </div>
      )}
    </div>
  );
};

export default ObserveWildlife;
