import React from 'react';

// Now accepts 'stats' prop directly so it doesn't need to fetch on every render
const PlayerStatus = ({ playerId, stats }) => {
  // If stats aren't passed (legacy usage), we could fetch, but Game.js now handles it.
  // We'll display what we have.
  
  const { name, health, score, inventory = [] } = stats || {};

  return (
    <div className="bg-gray-700/80 backdrop-blur-sm p-4 rounded-lg border border-gray-600 shadow-lg flex flex-wrap justify-around items-center gap-4 text-sm w-full">
      <div className="flex items-center space-x-2">
        <span className="text-gray-400 uppercase tracking-wider text-xs">Player</span>
        <span className="font-bold text-white">{name || 'Unknown'}</span>
      </div>
      
      <div className="flex items-center space-x-2">
        <span className="text-gray-400 uppercase tracking-wider text-xs">Health</span>
        <div className="w-24 bg-gray-600 rounded-full h-2.5">
          <div 
            className={`h-2.5 rounded-full ${health > 50 ? 'bg-green-500' : health > 20 ? 'bg-yellow-500' : 'bg-red-500'}`} 
            style={{ width: `${health || 0}%` }}
          ></div>
        </div>
        <span className="font-bold text-white">{health || 0}</span>
      </div>

      <div className="flex items-center space-x-2">
        <span className="text-gray-400 uppercase tracking-wider text-xs">Score</span>
        <span className="font-bold text-yellow-400">{score || 0}</span>
      </div>

      <div className="flex items-center space-x-2">
        <span className="text-gray-400 uppercase tracking-wider text-xs">Items</span>
        <span className="text-blue-300">
          {inventory.length > 0 ? inventory.join(', ') : 'None'}
        </span>
      </div>
    </div>
  );
};

export default PlayerStatus;
