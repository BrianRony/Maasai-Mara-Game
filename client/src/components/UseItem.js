import React, { useState } from 'react';

const UseItem = ({ playerId, onComplete, stats }) => {
  const [result, setResult] = useState('');
  const [itemName, setItemName] = useState('');
  
  // Get inventory from stats (passed from Game.js) or default to empty
  const inventory = stats?.inventory || [];

  const useItem = async () => {
    if (!itemName) {
      setResult("Please select an item.");
      return;
    }

    try {
      const response = await fetch('/api/use-item', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // Backend expects 'item_name' (snake_case) and 'player_id'
        body: JSON.stringify({ player_id: playerId, item_name: itemName }),
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data.message);
        
        // Progression
        setTimeout(() => {
          if (onComplete) onComplete(data.updated_stats || {});
        }, 6000);
      } else {
        const errorData = await response.json();
        setResult(`Error: ${errorData.message}`);
      }
    } catch (error) {
      console.error('Error using item:', error);
      setResult(`Error using item: ${error.message}`);
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg text-center">
      <h2 className="text-2xl font-bold text-yellow-500 mb-4">Use Inventory</h2>
      
      {inventory.length > 0 ? (
        <div className="mb-4">
          <select 
            value={itemName} 
            onChange={(e) => setItemName(e.target.value)}
            className="block w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-yellow-500 focus:border-yellow-500"
          >
            <option value="">-- Select an Item --</option>
            {inventory.map((item, index) => (
              <option key={index} value={item}>{item}</option>
            ))}
          </select>
        </div>
      ) : (
        <p className="text-gray-400 mb-4">Your inventory is empty.</p>
      )}

      <button
        onClick={useItem}
        disabled={!itemName}
        className={`font-bold py-2 px-4 rounded-md transition duration-300 ${
          itemName 
            ? 'bg-green-500 hover:bg-green-600 text-white' 
            : 'bg-gray-600 text-gray-400 cursor-not-allowed'
        }`}
      >
        Use Item
      </button>
      
      {result && (
        <div className="mt-4 p-4 bg-gray-700 rounded-md">
          <p className="text-yellow-400">{result}</p>
        </div>
      )}
    </div>
  );
};

export default UseItem;
