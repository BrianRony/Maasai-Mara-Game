import React, { useState, useEffect } from 'react';
import SafariLayout from './SafariLayout';

function Leaderboard() {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchPlayers();
  }, []);

  const fetchPlayers = async () => {
    try {
      const response = await fetch('/api/players');
      if (response.ok) {
        const data = await response.json();
        // Sort by score (descending)
        const sorted = data.sort((a, b) => b.score - a.score);
        setPlayers(sorted);
      } else {
        setError('Failed to load leaderboard');
      }
    } catch (err) {
      setError('Network error loading leaderboard');
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafariLayout title="Hall of Fame" subtitle="Top Explorers">
      <div className="max-w-4xl mx-auto">
        {loading && <p className="text-center text-yellow-500 animate-pulse">Loading scores...</p>}
        {error && <p className="text-center text-red-400">{error}</p>}

        {!loading && !error && (
          <div className="bg-gray-800 rounded-xl overflow-hidden shadow-2xl border border-gray-700">
            <table className="w-full text-left">
              <thead className="bg-gray-900 text-yellow-500 uppercase text-sm tracking-wider">
                <tr>
                  <th className="p-4 font-bold">Rank</th>
                  <th className="p-4 font-bold">Explorer</th>
                  <th className="p-4 font-bold">Class</th>
                  <th className="p-4 font-bold text-right">Score</th>
                  <th className="p-4 font-bold text-right">Health</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700 text-gray-300">
                {players.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="p-8 text-center text-gray-500 italic">
                      No adventurers yet. Be the first!
                    </td>
                  </tr>
                ) : (
                  players.map((player, index) => (
                    <tr 
                      key={player.uuid} 
                      className={`hover:bg-gray-700/50 transition-colors ${
                        index < 3 ? 'bg-yellow-900/10' : ''
                      }`}
                    >
                      <td className="p-4 font-mono text-yellow-600">
                        {index === 0 && '🥇'}
                        {index === 1 && '🥈'}
                        {index === 2 && '🥉'}
                        {index > 2 && `#${index + 1}`}
                      </td>
                      <td className="p-4 font-semibold text-white">{player.name}</td>
                      <td className="p-4 text-sm opacity-80">{player.character?.character_type || 'Unknown'}</td>
                      <td className="p-4 text-right font-bold text-yellow-400">{player.score}</td>
                      <td className="p-4 text-right font-mono">
                        <span className={player.health > 50 ? 'text-green-400' : 'text-red-400'}>
                          {player.health}%
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </SafariLayout>
  );
}

export default Leaderboard;
